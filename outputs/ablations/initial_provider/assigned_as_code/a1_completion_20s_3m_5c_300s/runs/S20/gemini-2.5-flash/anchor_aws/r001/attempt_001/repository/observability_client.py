import json
import os
from typing import Dict, Any, Optional

import boto3

from observability_models import LogEvent, QueryLogsRequest


class CloudWatchLogsClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("logs", region_name=self.region_name)

    def put_log_event(self, log_event: LogEvent):
        response = self.client.put_log_events(
            logGroupName=log_event.log_group,
            logStreamName=log_event.log_stream,
            logEvents=[
                {
                    "timestamp": log_event.timestamp_ms,
                    "message": json.dumps(log_event.message),
                }
            ],
        )
        if response.get("rejectedLogEventsInfo"):
            raise RuntimeError("The logging service rejected the event")
        return {"submitted": True}

    def query_log_events(self, query_request: QueryLogsRequest) -> Dict[str, Any]:
        # CloudWatch Logs Insights query syntax
        query_string = f"fields @timestamp, @message | sort @timestamp desc | limit {query_request.limit}"
        if query_request.filter_pattern:
            query_string = f"filter {query_request.filter_pattern} | {query_string}"

        start_query_response = self.client.start_query(
            logGroupName=query_request.log_group_name,
            startTime=query_request.start_time_ms,
            endTime=query_request.end_time_ms,
            queryString=query_string,
            limit=query_request.limit,
        )

        query_id = start_query_response["queryId"]

        response = None
        while response is None or response["status"] == "Running" or response["status"] == "Scheduled":
            # In a real application, you would add a delay here
            response = self.client.get_query_results(queryId=query_id)

        events = []
        for result in response["results"]:
            event = {}
            for field in result:
                event[field["field"]] = field["value"]
            events.append(event)

        return {"events": events}

