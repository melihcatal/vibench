import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List
from observability_client import CloudWatchLogsClient
from observability_models import LogEntry


def generate_correlation_id() -> str:
    return str(uuid.uuid4())


def write_correlated_logs(
    correlation_id: str,
    logs: List[Dict[str, Any]],
    log_stream_name: str = "application",
) -> Dict[str, Any]:
    client = CloudWatchLogsClient()

    results = []
    for log_data in logs:
        level = log_data.get("level", "INFO")
        message = log_data.get("message", "")
        service = log_data.get("service", "unknown")
        component = log_data.get("component", "unknown")

        log_entry = LogEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            level=level,
            message=message,
            correlation_id=correlation_id,
            service=service,
            component=component,
            metadata=log_data.get("metadata", {}),
        )

        log_message = log_entry.to_json()

        response = client.put_log_event(
            log_stream_name=log_stream_name,
            message=log_message,
            timestamp=int(time.time() * 1000),
        )

        results.append(
            {
                "level": level,
                "message": message,
                "sequence_token": response.get("nextSequenceToken", "unknown"),
                "success": True,
            }
        )

    return {
        "correlation_id": correlation_id,
        "logs_written": len(results),
        "results": results,
        "log_stream": log_stream_name,
        "log_group": client.log_group_name,
    }


def write_request_flow_logs(
    correlation_id: str,
    request_path: str,
    method: str,
    status_code: int,
    duration_ms: float,
    user_agent: str = None,
) -> Dict[str, Any]:
    logs = [
        {
            "level": "INFO",
            "message": f"Request started: {method} {request_path}",
            "service": "api-gateway",
            "component": "request-handler",
            "metadata": {
                "method": method,
                "path": request_path,
                "user_agent": user_agent,
            },
        },
        {
            "level": "INFO",
            "message": f"Processing request: {method} {request_path}",
            "service": "backend-service",
            "component": "request-processor",
            "metadata": {"correlation_id": correlation_id, "stage": "processing"},
        },
        {
            "level": "INFO" if status_code < 400 else "ERROR",
            "message": f"Request completed: {method} {request_path} - Status: {status_code}",
            "service": "api-gateway",
            "component": "response-handler",
            "metadata": {
                "status_code": status_code,
                "duration_ms": duration_ms,
                "correlation_id": correlation_id,
            },
        },
    ]

    return write_correlated_logs(correlation_id, logs)


def write_error_flow_logs(
    correlation_id: str,
    error_message: str,
    service: str,
    component: str,
    stack_trace: str = None,
) -> Dict[str, Any]:
    logs = [
        {
            "level": "ERROR",
            "message": f"Error occurred in {service}/{component}: {error_message}",
            "service": service,
            "component": component,
            "metadata": {
                "error_type": "application_error",
                "correlation_id": correlation_id,
            },
        },
        {
            "level": "WARNING",
            "message": f"Error handling initiated for correlation_id: {correlation_id}",
            "service": "error-handler",
            "component": "error-processor",
            "metadata": {"original_service": service, "original_component": component},
        },
    ]

    if stack_trace:
        logs.append(
            {
                "level": "DEBUG",
                "message": f"Stack trace for error: {stack_trace[:500]}...",
                "service": service,
                "component": component,
                "metadata": {"stack_trace_truncated": len(stack_trace) > 500},
            }
        )

    return write_correlated_logs(correlation_id, logs)


if __name__ == "__main__":
    correlation_id = generate_correlation_id()
    result = write_request_flow_logs(
        correlation_id=correlation_id,
        request_path="/api/users",
        method="GET",
        status_code=200,
        duration_ms=145.2,
        user_agent="Mozilla/5.0",
    )
    print(f"Correlated logs written: {result}")
