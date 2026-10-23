from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError


class LogQueryRequest:
    def __init__(self, log_group_name: str, query_string: str, start_time: int, end_time: int):
        self.log_group_name = log_group_name
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'logGroupName': self.log_group_name,
            'queryString': self.query_string,
            'startTime': self.start_time,
            'endTime': self.end_time
        }


class LogQueryResponse:
    def __init__(self, response: Dict[str, Any]):
        self.status = response.get('status', '')
        self.results = response.get('results', [])

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]) -> 'LogQueryResponse':
        return LogQueryResponse(response_dict)


def normalize_log_query_response(response: Dict[str, Any]) -> LogQueryResponse:
    return LogQueryResponse.from_dict(response)


def create_log_client() -> boto3.client:
    return boto3.client('logs')


def execute_log_query(client: boto3.client, request: LogQueryRequest) -> LogQueryResponse:
    try:
        response = client.start_query(
            logGroupName=request.log_group_name,
            queryString=request.query_string,
            startTime=request.start_time,
            endTime=request.end_time
        )
        query_id = response['queryId']
        get_query_results(client, query_id)
    except ClientError as e:
        print(f'Error executing log query: {e}')
        return LogQueryResponse({})


def get_query_results(client: boto3.client, query_id: str) -> LogQueryResponse:
    try:
        response = client.get_query_results(queryId=query_id)
        return normalize_log_query_response(response)
    except ClientError as e:
        print(f'Error getting query results: {e}')
        return LogQueryResponse({})
