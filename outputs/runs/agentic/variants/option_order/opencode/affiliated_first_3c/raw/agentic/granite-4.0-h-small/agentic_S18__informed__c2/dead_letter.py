import json
from messaging_client import MessagingClient


def dead_letter(message, reason):
    """Send a failed message to the dead-letter destination.

    Uses the same-scenario MessagingClient (IBM Event Streams) configured
    via IBM_EVENT_STREAMS_BROKERS and IBM_EVENT_STREAMS_APIKEY.

    Parameters:
        message (dict): Original message payload that failed processing.
        reason (str): Reason for failure to be included in the DLQ entry.
    """
    dlq_payload = {
        "original_message": message,
        "failure_reason": reason,
        "timestamp": "2025-08-15T12:34:56Z",
    }
    # DLQ topic can be hardcoded or configured elsewhere; here we use
    # a dedicated DLQ topic name.
    MessagingClient().publish("orders-dlq-topic", json.dumps(dlq_payload))


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    failed_msg = {
        "event_id": "e-9999",
        "type": "order_created",
        "error": "invalid_amount",
    }
    dead_letter(failed_msg, "Invalid amount in order payload")
