import os
import time
from observability_client import CloudWatchLogsClient

def query_error_logs(start_time_minutes_ago: int = 60, severity: str = "ERROR"):
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    log_group_name = os.environ.get("LOG_GROUP_NAME", "my-application-logs")

    client = CloudWatchLogsClient(region_name=region_name)

    end_time_ms = int(time.time() * 1000)
    start_time_ms = end_time_ms - (start_time_minutes_ago * 60 * 1000)

    query_string = f"fields @timestamp, @message | filter severity = '{severity}' | sort @timestamp desc"

    print(f"Starting CloudWatch Logs Insights query for error logs in group={log_group_name} from {start_time_minutes_ago} minutes ago.")
    query_response = client.start_query(
        log_group_names=[log_group_name],
        start_time=start_time_ms,
        end_time=end_time_ms,
        query_string=query_string
    )

    query_id = query_response['queryId']
    print(f"Query started with ID: {query_id}. Waiting for results...")

    status = 'Running'
    results = []
    while status in ['Running', 'Scheduled']:
        time.sleep(2) # Wait for 2 seconds before polling again
        query_results_response = client.get_query_results(query_id)
        status = query_results_response['status']
        print(f"Query status: {status}")

    if status == 'Complete':
        results = query_results_response['results']
        print(f"Found {len(results)} error logs.")
        for result in results:
            log_entry = {entry['field']: entry['value'] for entry in result}
            print(log_entry)
    else:
        print(f"Query failed or was cancelled. Final status: {status}")

    return results
