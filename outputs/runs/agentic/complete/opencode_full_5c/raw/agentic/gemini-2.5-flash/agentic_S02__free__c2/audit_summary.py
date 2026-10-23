import os
import boto3
from typing import Dict, Any, List


def summarize_audit_events(
    log_group_name: str, query_string: str
) -> List[Dict[str, Any]]:
    # boto3 and CloudWatch Logs client are identifiable signals for AWS provider
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    print(f"Starting CloudWatch Logs Insights query on log group: {{log_group_name}}")
    print(f"Query string: {{query_string}}")

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(
            os.getenv("START_TIME", "1678886400")
        ),  # Example timestamp (March 15, 2023 12:00:00 AM UTC)
        endTime=int(
            os.getenv("END_TIME", "1678972800")
        ),  # Example timestamp (March 16, 2023 12:00:00 AM UTC)
        queryString=query_string,
        limit=100,
    )

    query_id = start_query_response["queryId"]
    print(f"Query started with ID: {{query_id}}")

    response = None
    while response is None or response["status"] == "Running":
        print("Query is still running... waiting for results.")
        # In a real application, you would implement a delay here
        # For this example, we'll just loop quickly (not suitable for production)
        response = client.get_query_results(queryId=query_id)

    results = []
    for result_set in response["results"]:
        event = {}
        for field in result_set:
            event[field["field"]] = field["value"]
        results.append(event)

    print("Query results:")
    for r in results:
        print(r)
    return results


if __name__ == "__main__":
    # Ensure you have AWS credentials configured (e.g., via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # Example usage
    audit_log_group = os.environ.get(
        "AUDIT_LOG_GROUP", "/aws/lambda/your-audit-lambda"
    )  # Replace with your CloudWatch Log Group name
    # Example query to count login successes by user
    audit_query = "fields @timestamp, @message | filter event_type = 'federated_login' | stats count() by user_id, status"
    if audit_log_group == "/aws/lambda/your-audit-lambda":
        print(
            "Please configure AUDIT_LOG_GROUP environment variable to a real CloudWatch Log Group to test."
        )
    else:
        try:
            summarize_audit_events(audit_log_group, audit_query)
        except Exception as e:
            print(f"Error summarizing audit events: {e}")
