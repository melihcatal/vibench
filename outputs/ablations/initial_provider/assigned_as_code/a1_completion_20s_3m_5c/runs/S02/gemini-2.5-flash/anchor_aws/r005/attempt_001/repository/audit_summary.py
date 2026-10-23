import boto3
import os

def summarize_audit_events(log_group_name: str, query_string: str, start_time: int, end_time: int) -> list:
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        start_query_response = client.start_query(
            logGroupName=log_group_name,
            startTime=start_time, # Unix timestamp in seconds
            endTime=end_time, # Unix timestamp in seconds
            queryString=query_string,
            limit=1000
        )

        query_id = start_query_response["queryId"]

        response = None
        while response is None or response["status"] == "Running":
            print("Waiting for query to complete ...")
            import time
            time.sleep(1)
            response = client.get_query_results(queryId=query_id)

        results = []
        for result_set in response["results"]:
            record = {}
            for field in result_set:
                record[field["field"]] = field["value"]
            results.append(record)
        return results

    except Exception as e:
        raise RuntimeError(f"Error summarizing audit events with CloudWatch Logs Insights: {e}")
