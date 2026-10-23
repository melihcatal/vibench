import os
from datetime import datetime
from typing import Dict, List
from observability_client import get_logging_client
from observability_models import CorrelatedLogEvent


def write_correlated_logs(log_events: List[CorrelatedLogEvent]):
    """Write application log events with a shared correlation identifier to AWS CloudWatch Logs."""
    client = get_logging_client()

    # Group logs by their log group and stream
    log_groups = {}
    for event in log_events:
        key = (event.log_group, event.log_stream)
        if key not in log_groups:
            log_groups[key] = []
        log_groups[key].append(event)

    # Prepare and send logs to AWS CloudWatch Logs
    for (log_group, log_stream), events in log_groups.items():
        log_events_payload = []
        for event in events:
            log_events_payload.append(
                {
                    "timestamp": int(event.timestamp.timestamp() * 1000),
                    "message": json.dumps(
                        {
                            "message": event.message,
                            "severity": event.severity,
                            "correlation_id": event.correlation_id,
                            "service_name": event.service_name,
                            "tags": event.tags,
                            **event.custom_fields,
                        }
                    ),
                }
            )

        # Put log events to AWS CloudWatch Logs
        response = client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=log_events_payload,
        )

        response.raise_for_status()
