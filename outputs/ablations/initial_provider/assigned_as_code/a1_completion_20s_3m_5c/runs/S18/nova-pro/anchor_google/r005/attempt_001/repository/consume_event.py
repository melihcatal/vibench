import json

from google.cloud import pubsub_v1

def consume_event(config=None):
    config = config or {}
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(config["project_id"], config["subscription_id"])
    response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 1})
    if response.received_messages:
        message = response.received_messages[0]
        ack_id = message.ack_id
        data = json.loads(message.message.data.decode('utf-8'))
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [ack_id]})
        return data
    return None