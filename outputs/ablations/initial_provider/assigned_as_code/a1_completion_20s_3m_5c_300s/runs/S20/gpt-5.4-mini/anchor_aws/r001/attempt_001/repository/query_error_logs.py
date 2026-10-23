import json
import time

import boto3

from observability_client import load_config
from observability_models import parse_cw_log_event


def query_error_logs(config=None):
    config = load_config(config)
    client = boto3.client("logs", region_name=config.get("region"))
    end_ms = int(config.get("end_time_ms", time.time() * 1000))
    start_ms = int(config.get("start_time_ms", end_ms - 3600000))
    severities = config.get("severities", ["ERROR", "CRITICAL"])
    filters = ["severity = ERROR", "severity = CRITICAL"]
    if severities:
        filters = [f"severity = {severity}" for severity in severities]
    query_string = "fields @timestamp, @message | filter " + " or ".join(filters) + " | sort @timestamp desc | limit 50"
    response = client.start_query(
        logGroupName=config["log_group"],
        startTime=start_ms // 1000,
        endTime=end_ms // 1000,
        queryString=query_string,
    )
    query_id = response["queryId"]
    for _ in range(30):
        result = client.get_query_results(queryId=query_id)
        if result.get("status") == "Complete":
            rows = []
            for record in result.get("results", []):
                row = {item["field"]: item.get("value") for item in record}
                if "@message" in row:
                    row["parsed_message"] = parse_cw_log_event({"message": row["@message"]})
                rows.append(row)
            return {"query_id": query_id, "results": rows}
        time.sleep(1)
    raise RuntimeError("Timed out waiting for query completion")
