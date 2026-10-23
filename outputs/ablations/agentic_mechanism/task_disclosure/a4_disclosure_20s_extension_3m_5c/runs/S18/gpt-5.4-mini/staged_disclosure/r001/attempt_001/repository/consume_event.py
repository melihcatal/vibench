import json
import os
from google.cloud import pubsub_v1


def consume_event() -> str:
    project_id = os.environ["GCP_PROJECT_ID"]
    subscription_id = os.environ["GCP_PUBSUB_SUBSCRIPTION"]
    subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=10)
    if not response.received_messages:
        return ""
    received = response.received_messages[0]
    ack_id = received.ack_id
    message = received.message
    payload = message.data.decode("utf-8") if message.data else ""
    attributes = dict(message.attributes)
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])
    if attributes:
        return json.dumps({"data": payload, "attributes": attributes}, ensure_ascii=False)
    return payload


if __name__ == "__main__":
    print(consume_event())
