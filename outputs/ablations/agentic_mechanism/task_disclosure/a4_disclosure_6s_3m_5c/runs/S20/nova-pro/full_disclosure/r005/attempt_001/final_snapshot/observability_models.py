from typing import Any, Dict, List, Union

import boto3
from botocore.exceptions import ClientError


class LogQueryRequest:
    def __init__(self, log_group_name: str, query_string: str, start_time: int, end_time: int, limit: int = 20):
        self.log_group_name = log_group_name
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit


class LogQueryResponse:
    def __init__(self, status: str, results: List[Dict[str, Any]], statistics: Dict[str, Any]):
        self.status = status
        self.results = results
        self.statistics = statistics


def normalize_log_query_response(response: Dict[str, Any]) -> LogQueryResponse:
    try:
        status = response['status']
        results = response['results']
        statistics = response['statistics']
        return LogQueryResponse(status, results, statistics)
    except KeyError as e:
        raise ValueError(f'Invalid response format: {e}') from response


def execute_log_query(request: LogQueryRequest) -> LogQueryResponse:
    client = boto3.client('logs')
    try:
        response = client.start_query(
            logGroupName=request.log_group_name,
            queryString=request.query_string,
            startTime=request.start_time,
            endTime=request.end_time,
            limit=request.limit
        )
        query_id = response['queryId']
        while True:
            query_results = client.get_query_results(queryId=query_id)
            if query_results['status'] in ['Complete', 'Failed']:
                return normalize_log_query_response(query_results)
    except ClientError as e:
        raise RuntimeError(f'Error executing log query: {e}') from e
