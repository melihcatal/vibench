import os
import time
import json
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_logs_client

def query_error_logs(log_group_names: list[str], severity: str = "ERROR", minutes_ago: int = 60):
    client = get_cloudwatch_logs_client()

    end_time = int(time.time())
    start_time = int(end_time - (minutes_ago * 60))

    # CloudWatch Logs Insights query to filter for error logs
    # Assuming the structured log message is stored in the 'message' field as JSON
    query = f"fields @timestamp, @message | filter json_parse(@message).level = '{severity}' | sort @timestamp desc"

    start_query_response = client.start_query(
        logGroupNames=log_group_names,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
        limit=100
    )

    query_id = start_query_response['queryId']

    response = None
    while response is None or response['status'] == 'Running':
        time.sleep(1)  # Wait for the query to complete
        response = client.get_query_results(
            queryId=query_id
        )

    # Parse results
    error_logs = []
    for result_set in response['results']:
        log_entry = {}
        for field in result_set:
            if field['field'] == '@message':
                log_entry['message'] = json.loads(field['value'])
            else:
                log_entry[field['field'].replace('@', '')] = field['value']
        error_logs.append(log_entry)

    return error_logs

if __name__ == '__main__':
    LOG_GROUP = os.environ.get('LOG_GROUP_NAME', 'my-application-logs')
    
    print(f"Querying error logs for log group: {LOG_GROUP}...")
    errors = query_error_logs(log_group_names=[LOG_GROUP], severity="ERROR", minutes_ago=30)
    
    if errors:
        print(f"Found {len(errors)} error logs:")
        for error in errors:
            print(json.dumps(error, indent=2))
    else:
        print("No error logs found.")
