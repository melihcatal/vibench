import os
import json
import time
from typing import Dict, Any, List
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def get_logs_client():
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("logs", region_name=region)


def get_log_group():
    return os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/my-app")


def get_log_stream():
    return os.getenv("CLOUDWATCH_LOG_STREAM", "default-stream")


class CloudWatchLogWriter:
    def __init__(self, log_group: str = None, log_stream: str = None):
        self.client = get_logs_client()
        self.log_group = log_group or get_log_group()
        self.log_stream = log_stream or get_log_stream()
        self._ensure_stream()
        self.sequence_token = self._get_upload_sequence_token()

    def _ensure_stream(self):
        try:
            self.client.describe_log_streams(
                logGroupName=self.log_group, logStreamNames=[self.log_stream]
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                self.client.create_log_stream(
                    logGroupName=self.log_group, logStreamName=self.log_stream
                )
            else:
                raise

    def _get_upload_sequence_token(self):
        resp = self.client.describe_log_streams(
            logGroupName=self.log_group, logStreamNames=[self.log_stream]
        )
        log_streams = resp["logStreams"]
        if log_streams:
            return log_streams[0]["uploadSequenceToken"]
        return None

    def write(self, log_dict: Dict[str, Any]):
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        log_event = {"timestamp": timestamp, "message": json.dumps(log_dict)}
        kwargs = {
            "logGroupName": self.log_group,
            "logStreamName": self.log_stream,
            "logEvents": [log_event],
        }
        if self.sequence_token:
            kwargs["sequenceToken"] = self.sequence_token
        response = self.client.put_log_events(**kwargs)
        self.sequence_token = response["nextSequenceToken"]


class CloudWatchQuery:
    def __init__(self, log_group: str = None):
        self.client = get_logs_client()
        self.log_group = log_group or get_log_group()

    def query(
        self, query_string: str, start_time: int, end_time: int
    ) -> List[List[Dict[str, str]]]:
        response = self.client.start_query(
            logGroupName=self.log_group,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
        )
        query_id = response["queryId"]
        while True:
            results_response = self.client.get_query_results(queryId=query_id)
            status = results_response["status"]
            if status in ["Complete", "Failed", "Cancelled", "TimedOut"]:
                if status != "Complete":
                    raise ValueError(f"Query failed with status: {status}")
                return results_response["results"]
            time.sleep(0.5)
