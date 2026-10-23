import os
import json
from typing import Optional, Dict, Any
from messaging_client import PubSubClient
from messaging_models import MessagePayload, normalize_message_data


def consume_event(
    subscription_id: str, timeout: float = 5.0
) -> Optional[Dict[str, Any]]:
    client = PubSubClient()

    subscription_path = client.get_subscription_path(subscription_id)

    response = client.subscriber_client.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    message = received_message.message

    parsed_message = client.parse_message(message)

    try:
        payload = MessagePayload.from_dict(parsed_message["data"])
    except Exception:
        payload = normalize_message_data(parsed_message["data"])

    result = {
        "message_id": parsed_message["message_id"],
        "ack_id": received_message.ack_id,
        "payload": payload,
        "attributes": parsed_message["attributes"],
        "publish_time": parsed_message["publish_time"],
    }

    client.subscriber_client.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id],
        }
    )

    return result


def consume_and_process(
    subscription_id: str, processor_func, timeout: float = 5.0
) -> bool:
    message_data = consume_event(subscription_id, timeout)

    if not message_data:
        return False

    try:
        processor_func(message_data["payload"])
        return True
    except Exception as e:
        print(f"Failed to process message {message_data['message_id']}: {e}")
        return False


if __name__ == "__main__":

    def sample_processor(payload: MessagePayload):
        print(f"Processing event: {payload.event_type}")
        print(f"Data: {json.dumps(payload.data, indent=2)}")
        print(f"Source: {payload.source}")
        print(f"Timestamp: {payload.timestamp}")

    try:
        result = consume_event("user-events-subscription")
        if result:
            print(f"Consumed message ID: {result['message_id']}")
            sample_processor(result["payload"])
        else:
            print("No messages available")
    except Exception as e:
        print(f"Failed to consume event: {e}")
