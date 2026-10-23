import os
import json
from google.cloud import pubsub_v1


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    subscription_id = os.environ["PUBSUB_SUBSCRIPTION"]
    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project_id, subscription_id)
    response = client.pull(request={"subscription": subscription_path, "max_messages": 1, "return_immediately": True})
    if not response.received_messages:
        return
    received = response.received_messages[0]
    message = received.message
    payload = message.data.decode("utf-8") if message.data else ""
    try:
        output = json.loads(payload)
    except json.JSONDecodeError:
        output = payload
    print(output)
    client.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})


if __name__ == "__main__":
    main()
