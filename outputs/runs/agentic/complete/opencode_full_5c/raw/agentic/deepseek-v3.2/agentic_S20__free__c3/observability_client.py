import os
import json
from typing import Dict, Any, Optional, List
import boto3
from botocore.config import Config
from datetime import datetime, timedelta


class CloudWatchLogsClient:
    def __init__(self, log_group_name: str = None, region: str = None):
        self.log_group_name = log_group_name or os.getenv(
            "AWS_CLOUDWATCH_LOG_GROUP", "application-logs"
        )
        self.region = region or os.getenv("AWS_REGION", "us-east-1")

        config = Config(
            region_name=self.region, retries={"max_attempts": 3, "mode": "standard"}
        )

        self.client = boto3.client("logs", config=config)

    def put_log_event(
        self, log_stream_name: str, message: str, timestamp: int = None
    ) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = int(datetime.now().timestamp() * 1000)

        response = self.client.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=log_stream_name,
            logEvents=[{"timestamp": timestamp, "message": message}],
        )
        return response

    def start_query(
        self, query_string: str, start_time: int, end_time: int, limit: int = 100
    ) -> str:
        response = self.client.start_query(
            logGroupName=self.log_group_name,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=limit,
        )
        return response["queryId"]

    def get_query_results(self, query_id: str) -> Dict[str, Any]:
        response = self.client.get_query_results(queryId=query_id)
        return response

    def filter_log_events(
        self, filter_pattern: str, start_time: int, end_time: int, limit: int = 100
    ) -> List[Dict[str, Any]]:
        response = self.client.filter_log_events(
            logGroupName=self.log_group_name,
            filterPattern=filter_pattern,
            startTime=start_time,
            endTime=end_time,
            limit=limit,
        )
        return response.get("events", [])


def get_cloudwatch_client() -> CloudWatchLogsClient:
    return CloudWatchLogsClient()


def format_log_message(level: str, message: str, **kwargs) -> str:
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "message": message,
        **kwargs,
    }
    return json.dumps(log_entry)


def parse_log_message(log_message: str) -> Dict[str, Any]:
    try:
        return json.loads(log_message)
    except json.JSONDecodeError:
        return {"raw_message": log_message}


def get_time_range(minutes_ago: int = 15) -> tuple[int, int]:
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=minutes_ago)
    return int(start_time.timestamp() * 1000), int(end_time.timestamp() * 1000)
