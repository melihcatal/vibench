import os
import sys
import json
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import PullRequest


def get_subscription_path():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.getenv("PUBSUB_SUBSCRIPTION", "events-sub")
    subscriber = pubsub_v1.SubscriberClient()
    return subscriber.subscription_path(project_id, subscription_id)


if __name__ == "__main__":
    subscription_path = get_subscription_path()
    subscriber = pubsub_v1.SubscriberClient()
    request = PullRequest(subscription=subscription_path, max_messages=1)
    try:
        response = subscriber.pull(request=request, timeout=30.0)
        if not response.received_messages:
            print(json.dumps({"error": "No message received within timeout"}))
            sys.exit(0)
        received_message = response.received_messages[0]
        msg_data = {
            "message_id": received_message.message.message_id,
            "data": received_message.message.data.decode("utf-8"),
            "attributes": dict(received_message.message.attributes),
        }
        print(json.dumps(msg_data))
        subscriber.acknowledge(
            subscription=subscription_path, ack_ids=[received_message.ack_id]
        )
    except Exception as e:
        print(json.dumps({"error": str(e)}))
