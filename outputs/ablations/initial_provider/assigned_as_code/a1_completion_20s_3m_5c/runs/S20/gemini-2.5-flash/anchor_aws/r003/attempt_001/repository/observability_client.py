import os

import boto3

class ObservabilityClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.logs_client = boto3.client("logs", region_name=self.region_name)

    def put_log_events(self, log_group_name: str, log_stream_name: str, log_events: list):
        response = self.logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events,
        )
        if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
            raise RuntimeError("The logging service rejected the event")
        return {"submitted": True}

    def start_query(self, log_group_names: list, start_time: int, end_time: int, query_string: str, limit: int = 10000):
        response = self.logs_client.start_query(
            logGroupNames=log_group_names,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=limit,
        )
        return response

    def get_query_results(self, query_id: str):
        response = self.logs_client.get_query_results(queryId=query_id)
        return response
