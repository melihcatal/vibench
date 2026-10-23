import boto3
import os
import time
import json
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional

LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/demo/myapp")
LOG_STREAM = os.getenv("CLOUDWATCH_LOG_STREAM", "default")
REGION = os.getenv("AWS_REGION", "us-east-1")

logs_client = boto3.client("logs", region_name=REGION)


def ensure_resources():
    try:
        logs_client.create_log_group(logGroupName=LOG_GROUP)
    except ClientError:
        pass
    try:
        logs_client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
    except ClientError:
        pass


def get_upload_sequence_token() -> Optional[str]:
    streams = logs_client.describe_log_streams(
        logGroupName=LOG_GROUP, logStreamNamePrefix=LOG_STREAM
    )["logStreams"]
    if streams:
        return streams[0].get("uploadSequenceToken")
    return None


def put_structured_log(
    level: str,
    event_type: str,
    data: Dict[str, Any],
    correlation_id: Optional[str] = None,
) -> bool:
    ensure_resources()
    seq_token = get_upload_sequence_token()
    ts = int(time.time() * 1000)
    structured_data = {
        "level": level,
        "event": event_type,
        "data": data,
        "correlation_id": correlation_id,
        "@timestamp": ts,
    }
    log_event = {"timestamp": ts, "message": json.dumps(structured_data)}
    try:
        logs_client.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM,
            logEvents=[log_event],
            sequenceToken=seq_token,
        )
        return True
    except ClientError as e:
        if "InvalidSequenceTokenException" in str(e):
            new_token = get_upload_sequence_token()
            if new_token:
                logs_client.put_log_events(
                    logGroupName=LOG_GROUP,
                    logStreamName=LOG_STREAM,
                    logEvents=[log_event],
                    sequenceToken=new_token,
                )
                return True
        return False


def query_logs(
    filter_condition: str, start_time: int, end_time: int
) -> List[Dict[str, str]]:
    ensure_resources()
    query_string = f"fields @timestamp as `@timestamp`, @message as `@message`, $.level as level, $.correlation_id as correlation_id | filter {filter_condition}"
    response = logs_client.start_query(
        logGroupName=LOG_GROUP,
        startTime=start_time,
        endTime=end_time,
        queryString=query_string,
    )
    query_id = response["queryId"]
    while True:
        qresponse = logs_client.get_query_results(queryId=query_id)
        status = qresponse["status"]
        if status in ("Complete", "Failed", "TimedOut", "Cancelled"):
            break
        time.sleep(1)
    if status == "Complete" and "results" in qresponse:
        parsed_logs = []
        for row in qresponse["results"]:
            log_entry = {field["field"]: field["value"] for field in row}
            parsed_logs.append(log_entry)
        return parsed_logs
    return []
