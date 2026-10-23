import os
from typing import Dict, Any, Optional

from observability_client import CloudWatchLogsClient
from observability_models import CorrelatedLogEvent, LogEvent

def write_correlated_logs(
    correlation_id: str,
    log_messages: list[Dict[str, Any]],
    log_group: Optional[str] = None,
    log_stream: Optional[str] = None,
    region_name: Optional[str] = None,
):
    log_group = log_group or os.environ.get("LOG_GROUP_NAME", "my-application-logs")
    log_stream = log_stream or os.environ.get("LOG_STREAM_NAME", "default")
    client = CloudWatchLogsClient(region_name=region_name)

    results = []
    for message in log_messages:
        # Add correlation_id to each message within the 'event' field for consistency with write_structured_log.py
        # and to make it searchable in CloudWatch Logs Insights
        if "event" not in message:
            message["event"] = {}
        message["event"]["correlation_id"] = correlation_id

        event = CorrelatedLogEvent(
            correlation_id=correlation_id,
            message=message,
            log_group=log_group,
            log_stream=log_stream,
        )
        # Using the base LogEvent for `put_log_event` since the client expects `message` as Dict[str, Any]
        # and `CorrelatedLogEvent` is just a specialized form of `LogEvent` for internal representation.
        # The actual message content including correlation_id is embedded in `event.message`.
        log_event_for_client = LogEvent(
            timestamp_ms=event.timestamp_ms,
            message=event.message, # This already includes the correlation_id
            log_group=event.log_group,
            log_stream=event.log_stream,
        )
        results.append(client.put_log_event(log_event_for_client))
    return results
