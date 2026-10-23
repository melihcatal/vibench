import boto3
import os


class CloudWatchLogsClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION")
        if not self.region_name:
            raise ValueError("AWS_REGION must be provided or set in environment variables.")
        self.client = boto3.client("logs", region_name=self.region_name)

    def put_log_events(self, log_group_name, log_stream_name, log_events):
        response = self.client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events,
        )
        if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
            raise RuntimeError("The logging service rejected the event")
        return response

    def filter_log_events(self, log_group_name, start_time, end_time, filter_pattern=None, limit=None):
        params = {
            "logGroupName": log_group_name,
            "startTime": start_time,
            "endTime": end_time,
        }
        if filter_pattern:
            params["filterPattern"] = filter_pattern
        if limit:
            params["limit"] = limit
        
        response = self.client.filter_log_events(**params)
        return response.get("events", [])
