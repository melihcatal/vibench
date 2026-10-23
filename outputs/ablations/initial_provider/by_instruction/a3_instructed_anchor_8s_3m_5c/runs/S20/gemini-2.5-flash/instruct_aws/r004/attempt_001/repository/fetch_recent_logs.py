import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import get_cloudwatch_logs_client

def fetch_recent_logs(log_group_names: list[str], minutes_ago: int = 60, filters: Dict[str, Any] = None):
    client = get_cloudwatch_logs_client()

    end_time = int(time.time())
    start_time = int(end_time - (minutes_ago * 60))

    query_parts = ["fields @timestamp, @message"]
    if filters:
        for key, value in filters.items():
            # Assuming structured log messages are JSON strings in the 'message' field
            # And we are filtering on top-level keys within that JSON
            query_parts.append(f"filter json_parse(@message).{key} = '{value}'")
            
    query_parts.append("sort @timestamp desc")
    query = " | ".join(query_parts)

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
    recent_logs = []
    for result_set in response['results']:
        log_entry = {}
        for field in result_set:
            if field['field'] == '@message':
                try:
                    log_entry['message'] = json.loads(field['value'])
                except json.JSONDecodeError:
                    log_entry['message'] = field['value'] # If not JSON, keep as string
            else:
                log_entry[field['field'].replace('@', '')] = field['value']
        recent_logs.append(log_entry)

    return recent_logs

if __name__ == '__main__':
    LOG_GROUP = os.environ.get('LOG_GROUP_NAME', 'my-application-logs')

    print(f"Fetching recent logs for log group: {LOG_GROUP} with a filter...")
    # Example: Fetch logs where service is 'user-service'
    filters = {"service": "user-service"}
    logs = fetch_recent_logs(log_group_names=[LOG_GROUP], minutes_ago=60, filters=filters)

    if logs:
        print(f"Found {len(logs)} recent logs:")
        for log_entry in logs:
            print(json.dumps(log_entry, indent=2))
    else:
        print("No recent logs found with the specified filters.")

    print(f"\nFetching all recent logs for log group: {LOG_GROUP} (no filters)...")
    all_logs = fetch_recent_logs(log_group_names=[LOG_GROUP], minutes_ago=60)
    if all_logs:
        print(f"Found {len(all_logs)} recent logs:")
        # print first 5 for brevity
        for log_entry in all_logs[:5]: 
            print(json.dumps(log_entry, indent=2))
    else:
        print("No recent logs found.")
