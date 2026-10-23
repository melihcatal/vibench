import json
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from observability_client import get_datadog_client
from observability_models import StructuredLog

def send_structured_log(log_event: StructuredLog):
    """
    Sends a single structured log event to Datadog.

    Args:
        log_event: A StructuredLog object representing the log.
    """
    logs_api = get_datadog_client()

    log_payload = HTTPLog(
        [
            HTTPLogItem(
                **log_event.to_datadog_payload()
            ),
        ]
    )

    try:
        logs_api.submit_log(log_payload)
        print("Successfully sent structured log to Datadog.")
    except Exception as e:
        print(f"Error sending log to Datadog: {e}")

# Example of how to create and send a log is omitted as per instructions.
