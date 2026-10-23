import boto3


def summarize_audit_events(log_group: str, query: str) -> dict:
    client = boto3.client("logs")
    resp = client.start_query(logGroupName=log_group, startTime=0, endTime=9999999999, queryString=query)
    return {"provider": "AWS CloudWatch Logs", "query_id": resp["queryId"]}
