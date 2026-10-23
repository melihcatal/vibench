import boto3
import os
import time
from botocore.exceptions import ClientError
from .observability_models import (
    CloudWatchLogEvent,
    QueryParams,
    cloudwatch_result_to_dict,
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
LOG_GROUP = os.getenv("LOG_GROUP_NAME", "/aws/lambda/app-logs")
LOG_STREAM = os.getenv("LOG_STREAM_NAME", "default")

logs_client = boto3.client("logs", region_name=AWS_REGION)


def create_log_stream_if_not_exists():
    try:
        logs_client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code != "ResourceAlreadyExistsException":
            raise


def get_upload_sequence_token() -> Optional[str]:
    try:
        resp = logs_client.describe_log_streams(
            logGroupName=LOG_GROUP, logStreamName=LOG_STREAM
        )
        if resp["logStreams"]:
            return resp["logStreams"][0].get("uploadSequenceToken")
    except ClientError:
        pass
    return None


def put_log_events(
    events: List[CloudWatchLogEvent], sequence_token: Optional[str] = None
) -> Optional[str]:
    create_log_stream_if_not_exists()
    params = {
        "logEvents": [{"timestamp": e.timestamp, "message": e.message} for e in events],
        "logGroupName": LOG_GROUP,
        "logStreamName": LOG_STREAM,
    }
    if sequence_token:
        params["sequenceToken"] = sequence_token
    resp = logs_client.put_log_events(**params)
    return resp.get("nextSequenceToken")


def query_logs(query_params: QueryParams) -> List[Dict[str, Any]]:
    start_resp = logs_client.start_query(
        logGroupName=LOG_GROUP,
        startTime=query_params.start_time,
        endTime=query_params.end_time,
        queryString=query_params.query,
    )
    query_id = start_resp["queryId"]

    while True:
        time.sleep(0.5)
        result = logs_client.get_query_results(queryId=query_id)
        status = result["status"]
        if status == "Complete":
            return cloudwatch_result_to_dict(result)
        if status == "Failed":
            raise RuntimeError(
                f"Query failed: {result.get('errorMessage', 'Unknown error')}"
            )
