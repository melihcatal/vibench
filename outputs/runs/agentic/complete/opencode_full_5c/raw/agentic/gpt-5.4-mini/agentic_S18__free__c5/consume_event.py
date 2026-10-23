import json
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_subscription_path, load_messaging_config
from messaging_models import ConsumeResult, decode_message, normalize_message_record


def consume_event(timeout=10):
    config = load_messaging_config()
    client = get_subscriber_client()
    subscription_path = get_subscription_path(client, config.project_id, config.subscription_id)
    response = client.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True}, timeout=timeout)
    if not response.received_messages:
        return ConsumeResult.empty(subscription_path)
    received = response.received_messages[0]
    record = decode_message(received.message)
    client.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})
    return ConsumeResult(message=normalize_message_record(record), subscription=subscription_path)


if __name__ == '__main__':
    result = consume_event()
    print(result.to_json())
