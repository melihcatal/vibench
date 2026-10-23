import os
import boto3
from typing import List, Dict, Any

def summarize_audit_events(
    log_group_name: str,
    query_string: str,
    start_time: int, # Unix timestamp in seconds
    end_time: int # Unix timestamp in seconds
) -> List[Dict[str, Any]]:
    
    # Initialize AWS CloudWatch Logs client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as environment variables
    # or configured in ~/.aws/credentials
    try:
        client = boto3.client('logs', region_name=os.environ.get("AWS_REGION", "us-east-1"))
    except Exception as e:
        print(f"Error initializing boto3 client: {e}. Ensure AWS credentials and region are configured.")
        return []

    try:
        # Start the CloudWatch Logs Insights query
        start_query_response = client.start_query(
            logGroupName=log_group_name,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=100  # Max 100 results for this example
        )
        query_id = start_query_response['queryId']
        print(f"Started CloudWatch Logs Insights query with ID: {query_id}")

        # Poll for query results
        response = None
        while response is None or response['status'] == 'Running':
            print("Query still running...")
            import time
            time.sleep(2) # Wait for 2 seconds before polling again
            response = client.get_query_results(queryId=query_id)

        if response['status'] == 'Complete':
            print("Query completed successfully.")
            # Process the results
            results = []
            for r in response['results']:
                event = {}
                for field in r:
                    event[field['field']] = field['value']
                results.append(event)
            return results
        else:
            print(f"CloudWatch Logs Insights query failed with status: {response['status']}")
            return []

    except Exception as e:
        print(f"Error querying CloudWatch Logs Insights: {e}")
        return []

if __name__ == "__main__":
    # Example usage: Ensure AWS credentials and region are set in your environment
    # os.environ["AWS_ACCESS_KEY_ID"] = "YOUR_AWS_ACCESS_KEY_ID"
    # os.environ["AWS_SECRET_ACCESS_KEY"] = "YOUR_AWS_SECRET_ACCESS_KEY"
    # os.environ["AWS_REGION"] = "us-east-1"

    example_log_group = "/aws/vendedlogs/myloggroup"
    # A sample query to count login events by user
    example_query = "fields @timestamp, @message | filter @message like /Federated login/ | stats count() by user_id"
    import time
    # Last 1 hour
    end_time = int(time.time())
    start_time = end_time - 3600

    print(f"Summarizing audit events from log group: {example_log_group}")
    summary_results = summarize_audit_events(example_log_group, example_query, start_time, end_time)

    if summary_results:
        print("\n--- Audit Summary Results ---")
        for item in summary_results:
            print(item)
    else:
        print("No audit summary results found or an error occurred.")
