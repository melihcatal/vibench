import os
import time
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient

def query_error_logs(severity: str = "ERROR", hours_ago: int = 1):
    client = ObservabilityClient()
    cloudwatch_logs_client = client.get_client()
    log_group_name = client.get_log_group_name()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)

    query_string = f"fields @timestamp, @message | filter severity = '{severity}' | sort @timestamp desc"

    try:
        start_query_response = cloudwatch_logs_client.start_query(
            logGroupName=log_group_name,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            queryString=query_string,
            limit=100
        )
        query_id = start_query_response['queryId']

        print(f"Started CloudWatch Logs Insights query with ID: {query_id}")

        response = None
        while response is None or response['status'] == 'Running' or response['status'] == 'Scheduled':
            time.sleep(1) # Wait for 1 second before checking again
            response = cloudwatch_logs_client.get_query_results(queryId=query_id)

        if response['status'] == 'Complete':
            error_logs = []
            for result in response['results']:
                log_entry = {}
                for field in result:
                    log_entry[field['field']] = field['value']
                error_logs.append(log_entry)
            print(f"Found {len(error_logs)} error logs with severity '{severity}' in the last {hours_ago} hours.")
            for log in error_logs:
                print(log)
            return error_logs
        else:
            print(f"CloudWatch Logs Insights query failed with status: {response['status']}")
            return []

    except Exception as e:
        print(f"Error querying error logs from AWS CloudWatch Logs: {e}")
        return []

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     query_error_logs(severity="ERROR", hours_ago=24)
