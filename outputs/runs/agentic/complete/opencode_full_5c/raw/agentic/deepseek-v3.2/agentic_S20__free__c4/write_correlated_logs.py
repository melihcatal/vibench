import json
import uuid
from datetime import datetime
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

from observability_client import client
from observability_models import LogEvent, LogLevel
from write_structured_log import write_structured_log


def write_correlated_logs(
    correlation_id: str = None,
    log_messages: List[Dict[str, Any]] = None,
    component: str = "api",
) -> Dict[str, Any]:
    """
    Write multiple application log events that share a correlation identifier.

    Args:
        correlation_id: Shared correlation/request ID (generated if not provided)
        log_messages: List of dicts with 'message' and 'level' keys
        component: Application component name

    Returns:
        Dictionary with write results
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    if log_messages is None:
        log_messages = [
            {
                "message": f"Request started with correlation ID: {correlation_id}",
                "level": LogLevel.INFO,
            },
            {"message": "Processing request data", "level": LogLevel.DEBUG},
            {"message": "Request completed successfully", "level": LogLevel.INFO},
        ]

    results = []
    all_success = True

    for i, log_msg in enumerate(log_messages):
        message = log_msg.get("message", f"Log entry {i + 1}")
        level = log_msg.get("level", LogLevel.INFO)

        extra_fields = {
            "correlation_id": correlation_id,
            "log_sequence": i + 1,
            "total_logs": len(log_messages),
        }

        if "extra_fields" in log_msg:
            extra_fields.update(log_msg["extra_fields"])

        result = write_structured_log(
            message=message, level=level, extra_fields=extra_fields, component=component
        )

        results.append(result)
        if not result.get("success", False):
            all_success = False

    try:
        log_stream_name = client.get_log_stream_name(component)

        cloudwatch_response = client.cloudwatch_logs_client.describe_log_streams(
            logGroupName=client._log_group_name,
            logStreamNamePrefix=log_stream_name,
            limit=1,
        )

        log_stream_info = cloudwatch_response.get("logStreams", [])
        if log_stream_info:
            stream_name = log_stream_info[0]["logStreamName"]
            print(f"Correlated logs written to CloudWatch stream: {stream_name}")
        else:
            print(f"Correlated logs written with correlation ID: {correlation_id}")

    except ClientError as e:
        print(f"Note: Could not verify CloudWatch log stream: {e}")

    return {
        "success": all_success,
        "correlation_id": correlation_id,
        "total_logs": len(log_messages),
        "successful_logs": sum(1 for r in results if r.get("success", False)),
        "failed_logs": sum(1 for r in results if not r.get("success", False)),
        "results": results,
    }


def write_distributed_trace_logs(
    correlation_id: str, service_calls: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Write logs for distributed trace across multiple services.

    Args:
        correlation_id: Shared correlation ID across services
        service_calls: List of service call events

    Returns:
        Dictionary with write results
    """
    log_messages = []

    for i, call in enumerate(service_calls):
        service = call.get("service", f"service-{i + 1}")
        operation = call.get("operation", "process")
        duration = call.get("duration_ms", 0)
        success = call.get("success", True)

        level = LogLevel.INFO if success else LogLevel.ERROR
        message = f"{service}: {operation} {'completed' if success else 'failed'} in {duration}ms"

        log_messages.append(
            {
                "message": message,
                "level": level,
                "extra_fields": {
                    "service": service,
                    "operation": operation,
                    "duration_ms": duration,
                    "success": success,
                    "trace_order": i + 1,
                },
            }
        )

    return write_correlated_logs(
        correlation_id=correlation_id,
        log_messages=log_messages,
        component="distributed-trace",
    )
