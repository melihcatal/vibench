import os
import boto3
import json
import time

# AWS CloudWatch Logs Insights Configuration
AWS_REGION = os.environ.get("AWS_REGION")
CLOUDWATCH_LOG_GROUP_NAME = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME")

def summarize_login_audit_events(start_time_seconds: int, end_time_seconds: int):
    """
    Summarizes federated login audit events using AWS CloudWatch Logs Insights.
    The query looks for logs containing "FederatedLogin" and provides a count by outcome and provider.
    """
    if not all([AWS_REGION, CLOUDWATCH_LOG_GROUP_NAME]):
        raise ValueError("Missing AWS CloudWatch Logs Insights configuration environment variables.")

    client = boto3.client('logs', region_name=AWS_REGION)

    query_string = """
    fields @timestamp, @message
    | filter @message like /FederatedLogin/
    | parse @message "outcome=*" as outcome
    | parse @message "provider=*" as provider
    | stats count() by outcome, provider
    | sort by count() desc
    """

    try:
        start_query_response = client.start_query(
            logGroupName=CLOUDWATCH_LOG_GROUP_NAME,
            startTime=start_time_seconds,
            endTime=end_time_seconds,
            queryString=query_string,
            limit=100 # Max number of results
        )

        query_id = start_query_response['queryId']
        print(f"Started CloudWatch Logs Insights query with ID: {query_id}")

        response = None
        while response is None or response['status'] == 'Running':
            time.sleep(1) # Wait for the query to complete
            response = client.get_query_results(queryId=query_id)

        if response['status'] == 'Complete':
            results = []
            for result_set in response['results']:
                entry = {}
                for field in result_set:
                    entry[field['field']] = field['value']
                results.append(entry)
            return results
        else:
            print(f"CloudWatch Logs Insights query failed or cancelled. Status: {response['status']}")
            return None

    except Exception as e:
        print(f"Error querying CloudWatch Logs Insights: {e}")
        return None

if __name__ == "__main__":
    # Example usage: last 1 hour
    end_time = int(time.time())
    start_time = end_time - 3600 # 1 hour ago

    # For a real run, ensure AWS_REGION and CLOUDWATCH_LOG_GROUP_NAME are set.
    # summary = summarize_login_audit_events(start_time, end_time)
    # if summary:
    #     print("Login Audit Summary:")
    #     print(json.dumps(summary, indent=2))
    # else:
    #     print("Failed to get audit summary.")
    print("To test, ensure AWS credentials and environment variables are set and call summarize_login_audit_events.")
