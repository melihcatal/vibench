import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

from observability_client import client
from observability_models import LogEvent, LogLevel


def write_structured_log(
    message: str,
    level: LogLevel = LogLevel.INFO,
    extra_fields: Optional[Dict[str, Any]] = None,
    component: str = "default",
) -> Dict[str, Any]:
    """
    Write a structured JSON log event to AWS CloudWatch Logs.

    Args:
        message: The log message
        level: Log severity level
        extra_fields: Additional structured fields to include
        component: Application component name for log stream

    Returns:
        Dictionary with write result including sequence token
    """
    try:
        log_event = LogEvent(
            message=message,
            level=level,
            timestamp=datetime.utcnow(),
            service=os.getenv("SERVICE_NAME", "unknown-service"),
            environment=os.getenv("ENVIRONMENT", "development"),
            extra_fields=extra_fields,
        )

        event_dict = log_event.to_dict()
        log_stream_name = client.get_log_stream_name(component)

        log_event_batch = {
            "logGroupName": client._log_group_name,
            "logStreamName": log_stream_name,
            "logEvents": [
                {
                    "timestamp": int(datetime.utcnow().timestamp() * 1000),
                    "message": json.dumps(event_dict),
                }
            ],
        }

        response = client.cloudwatch_logs_client.put_log_events(**log_event_batch)

        print(f"Successfully wrote structured log to CloudWatch: {log_stream_name}")
        print(f"Message: {message}")
        print(f"Level: {level.value}")

        if extra_fields:
            print(f"Extra fields: {extra_fields}")

        return {
            "success": True,
            "log_stream": log_stream_name,
            "next_sequence_token": response.get("nextSequenceToken"),
            "event": event_dict,
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            try:
                client.cloudwatch_logs_client.create_log_stream(
                    logGroupName=client._log_group_name, logStreamName=log_stream_name
                )
                response = client.cloudwatch_logs_client.put_log_events(
                    **log_event_batch
                )

                print(f"Created log stream and wrote structured log: {log_stream_name}")
                return {
                    "success": True,
                    "log_stream": log_stream_name,
                    "next_sequence_token": response.get("nextSequenceToken"),
                    "event": event_dict,
                }
            except ClientError as create_error:
                print(f"Failed to create log stream: {create_error}")
                return {
                    "success": False,
                    "error": str(create_error),
                    "error_code": create_error.response["Error"]["Code"],
                }
        else:
            print(f"Failed to write structured log to CloudWatch: {e}")
            return {"success": False, "error": str(e), "error_code": error_code}
    except Exception as e:
        print(f"Unexpected error writing structured log: {e}")
        return {"success": False, "error": str(e)}
