import boto3

from observability_client import load_config
from observability_models import normalize_result


def query_error_logs(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("logs", region_name=cfg["region"])
    query = payload.get("query") or "fields @timestamp, @message | filter severity = 'error'"
    response = client.start_query(
        logGroupNames=[cfg["log_group"]],
        startTime=payload["start_time"],
        endTime=payload["end_time"],
        queryString=query,
    )
    results = client.get_query_results(queryId=response["queryId"])
    return normalize_result(results)
