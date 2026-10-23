import json
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_CONFIG
from messaging_models import MessageEvent


def consume_event():
    project_id = PUBSUB_CONFIG["project_id"]
    subscription_id = PUBSUB_CONFIG["subscription_id"]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    response = subscriber.pull(
        subscription=subscription_path, max_messages=1, return_immediately=True
    )
    if not response.received_messages:
        print("No messages.")
        return None
    message = response.received_messages[0]
    data_str = message.message.data.decode("utf-8")
    data = json.loads(data_str)
    event = MessageEvent.model_validate(data)
    print(f"Consumed event: {event.event_id}")
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[message.ack_id])
    return event


if __name__ == "__main__":
    consume_event()
