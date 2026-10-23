import os
import time
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient

def fetch_recent_logs(field_filters: dict = None, hours_ago: int = 1, limit: int = 100):
    client = ObservabilityClient()
    cloudwatch_logs_client = client.get_client()
    log_group_name = client.get_log_group_name()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)

    query_string = "fields @timestamp, @message"
    if field_filters:
        filter_clauses = []
        for field, value in field_filters.items():
            filter_clauses.append(f"filter {field} = '{value}'")
        query_string += " | " + " | ".join(filter_clauses)

    query_string += " | sort @timestamp desc"

    try:
        start_query_response = cloudwatch_logs_client.start_query(
            logGroupName=log_group_name,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            queryString=query_string,
            limit=limit
        )
        query_id = start_query_response['queryId']

        print(f"Started CloudWatch Logs Insights query with ID: {query_id}")

        response = None
        while response is None or response['status'] == 'Running' or response['status'] == 'Scheduled':
            time.sleep(1) # Wait for 1 second before checking again
            response = cloudwatch_logs_client.get_query_results(queryId=query_id)

        if response['status'] == 'Complete':
            recent_logs = []
            for result in response['results']:
                log_entry = {}
                for field in result:
                    log_entry[field['field']] = field['value']
                recent_logs.append(log_entry)
            print(f"Found {len(recent_logs)} recent logs filtered by {field_filters} in the last {hours_ago} hours.")
            for log in recent_logs:
                print(log)
            return recent_logs
        else:
            print(f"CloudWatch Logs Insights query failed with status: {response['status']}")
            return []

    except Exception as e:
        print(f"Error fetching recent logs from AWS CloudWatch Logs: {e}")
        return []

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     # Fetch all logs from a specific service in the last 2 hours
#     fetch_recent_logs(field_filters={"service": "authentication-service"}, hours_ago=2)
#     # Fetch all logs with a specific severity in the last 1 hour
#     fetch_recent_logs(field_filters={"severity": "INFO"})
