import boto3
import json
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_logs_client


def fetch_recent_logs(log_group_name, field_filters=None, hours_back=1, limit=50):
    """
    Retrieve recent log results filtered by field values and time range from AWS CloudWatch Logs.

    Args:
        log_group_name: CloudWatch Logs group name
        field_filters: Dictionary of field:value pairs to filter by
        hours_back: Number of hours to look back
        limit: Maximum number of results to return
    """
    client = get_cloudwatch_logs_client()

    # Calculate time range
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(hours=hours_back)).timestamp() * 1000)

    # Build query with field filters
    query_parts = ["fields @timestamp, @message, @logStream, @log"]

    if field_filters:
        filter_conditions = []
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_conditions.append(f'@message like /"{field}":.*"{value}"/')
            else:
                filter_conditions.append(f'@message like /"{field}":{value}/')

        if filter_conditions:
            query_parts.append(f"| filter {' and '.join(filter_conditions)}")

    query_parts.append(f"| sort @timestamp desc")
    query_parts.append(f"| limit {limit}")

    query = "\n".join(query_parts)

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
            "field_filters": field_filters,
            "time_range": {
                "start": start_time,
                "end": end_time,
                "hours_back": hours_back,
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
