import time
import datetime
import os
import json

from observability_client import ObservabilityClient
from observability_models import LogQuery, QueryResult

def fetch_recent_logs(query_request: LogQuery, config=None) -> QueryResult:
    config = config or {}
    client = ObservabilityClient(region_name=config.get("region"))

    start_time_ms = int(query_request.start_time.timestamp() * 1000)
    end_time_ms = int(query_request.end_time.timestamp() * 1000)

    query_string = f"fields @timestamp, @message | sort @timestamp desc | limit {query_request.limit}"
    if query_request.filter_pattern:
        query_string = f"fields @timestamp, @message | filter {query_request.filter_pattern} | sort @timestamp desc | limit {query_request.limit}"

    start_query_response = client.start_query(
        log_group_names=[query_request.log_group_name],
        start_time=start_time_ms,
        end_time=end_time_ms,
        query_string=query_string,
        limit=query_request.limit
    )

    query_id = start_query_response["queryId"]

    while True:
        query_results_response = client.get_query_results(query_id)
        status = query_results_response["status"]
        if status != "Running" and status != "Scheduled":
            break
        time.sleep(1) # Wait for a second before polling again

    fields = []
    records = []
    if "results" in query_results_response:
        for result in query_results_response["results"]:
            record = {}
            for field in result:
                record[field["field"]] = field["value"]
            records.append(record)

        if records:
            for field_name in records[0].keys():
                fields.append({"name": field_name, "type": "string"})

    return QueryResult(fields=fields, records=records)
