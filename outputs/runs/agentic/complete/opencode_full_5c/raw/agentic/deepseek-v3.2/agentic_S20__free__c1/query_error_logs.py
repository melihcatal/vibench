import boto3
import json
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_logs_client


def query_error_logs(log_group_name, severity="ERROR", hours_back=24, limit=100):
    """
    Query recent error log entries filtered by severity and time range from AWS CloudWatch Logs.

    Args:
        log_group_name: CloudWatch Logs group name
        severity: Log severity level to filter (ERROR, WARN, etc.)
        hours_back: Number of hours to look back
        limit: Maximum number of results to return
    """
    client = get_cloudwatch_logs_client()

    # Calculate time range
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(hours=hours_back)).timestamp() * 1000)

    # Construct query to filter by severity
    query = f"""
    fields @timestamp, @message, @logStream, @log
    | filter @message like /{severity}/i
    | sort @timestamp desc
    | limit {limit}
    """

    try:
        # Start query
        start_response = client.start_query(
            logGroupName=log_group_name,
            startTime=start_time,
            endTime=end_time,
            queryString=query,
            limit=limit,
        )

        query_id = start_response["queryId"]

        # Wait for query to complete
        import time

        for _ in range(30):  # Wait up to 30 seconds
            response = client.get_query_results(queryId=query_id)
            if response["status"] in ["Complete", "Failed", "Cancelled"]:
                break
            time.sleep(1)

        if response["status"] != "Complete":
            return {
                "success": False,
                "error": f"Query {response['status']}",
                "query_id": query_id,
            }

        # Parse results
        results = []
        for result in response.get("results", []):
            parsed_result = {}
            for field in result:
                parsed_result[field["field"]] = field["value"]

            # Parse JSON message if possible
            if "@message" in parsed_result:
                try:
                    message_data = json.loads(parsed_result["@message"])
                    parsed_result["parsed_message"] = message_data
                except:
                    parsed_result["parsed_message"] = parsed_result["@message"]

            results.append(parsed_result)

        return {
            "success": True,
            "query_id": query_id,
            "results": results,
            "result_count": len(results),
            "severity": severity,
            "time_range": {
                "start": start_time,
                "end": end_time,
                "hours_back": hours_back,
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
