import json
import os
import time
from typing import Dict, Any
from observability_client import get_cloudwatch_logs_client
from observability_models import StructuredLogMessage, LogEvent

def write_correlated_log(log_group_name: str, log_stream_name: str, message: StructuredLogMessage):
    client = get_cloudwatch_logs_client()

    log_event = LogEvent(
        timestamp=int(time.time() * 1000),
        message=json.dumps(message.__dict__)
    )

    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event.__dict__]
    )
    return response

if __name__ == '__main__':
    LOG_GROUP = os.environ.get('LOG_GROUP_NAME', 'my-application-logs')
    LOG_STREAM = os.environ.get('LOG_STREAM_NAME', 'my-instance-stream')

    correlation_id = "req-1234567890"

    # First log event in a correlated series
    log_message_1 = StructuredLogMessage(
        level="INFO",
        service="payment-service",
        event="payment_initiated",
        timestamp=time.time(),
        correlation_id=correlation_id,
        user_id="user-abc",
        details={
            "order_id": "order-001",
            "amount": 100.00
        }
    )
    response_1 = write_correlated_log(LOG_GROUP, LOG_STREAM, log_message_1)
    print(f"Correlated log event 1 written: {response_1}")

    # Second log event in the same correlated series
    log_message_2 = StructuredLogMessage(
        level="INFO",
        service="inventory-service",
        event="item_reserved",
        timestamp=time.time(),
        correlation_id=correlation_id,
        details={
            "order_id": "order-001",
            "item_sku": "XYZ123",
            "quantity": 1
        }
    )
    response_2 = write_correlated_log(LOG_GROUP, LOG_STREAM, log_message_2)
    print(f"Correlated log event 2 written: {response_2}")
