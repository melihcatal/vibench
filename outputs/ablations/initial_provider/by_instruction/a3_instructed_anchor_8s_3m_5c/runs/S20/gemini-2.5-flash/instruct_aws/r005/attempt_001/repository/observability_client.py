import os
import boto3
from typing import Dict, Any, List

class ObservabilityClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get('AWS_REGION', 'us-east-1')
        self.cloudwatch_logs_client = boto3.client('logs', region_name=self.region_name)

    def put_log_events(self, log_group_name: str, log_stream_name: str, log_events: List[Dict[str, Any]]):
        response = self.cloudwatch_logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        return response

    def start_query(self, log_group_names: List[str], start_time: int, end_time: int, query_string: str) -> str:
        response = self.cloudwatch_logs_client.start_query(
            logGroupNames=log_group_names,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=1000
        )
        return response['queryId']

    def get_query_results(self, query_id: str) -> Dict[str, Any]:
        response = self.cloudwatch_logs_client.get_query_results(
            queryId=query_id
        )
        return response

