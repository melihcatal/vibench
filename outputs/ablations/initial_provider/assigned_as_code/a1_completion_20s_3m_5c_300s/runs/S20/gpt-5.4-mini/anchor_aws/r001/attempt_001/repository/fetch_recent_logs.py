import time

import boto3

from observability_client import load_config
from observability_models import parse_cw_log_event


def fetch_recent_logs(config=None):
    config = load_config(config)
    client = boto3.client("logs", region_name=config.get("region"))
    end_ms = int(config.get("end_time_ms", time.time() * 1000))
    start_ms = int(config.get("start_time_ms", end_ms - 900000))
    filters = config.get("field_filters", {})
    clauses = []
    for key, value in filters.items():
        clauses.append(f'{key} = "{value}"')
    query_string = "fields @timestamp, @message"
    if clauses:
        query_string += " | filter " + " and ".join(clauses)
    query_string += " | sort @timestamp desc | limit 100"
    response = client.start_query(
        logGroupName=config["log_group"],
        startTime=start_ms // 1000,
        endTime=end_ms // 1000,
        queryString=query_string,
    )
    query_id = response["queryId"]
    while True:
        result = client.get_query_results(queryId=query_id)
        if result.get("status") == "Complete":
            return {
                "query_id": query_id,
                "results": [parse_cw_log_event({item["field"]: item.get("value") for item in record}) for record in result.get("results", [])],
            }
        time.sleep(1)
