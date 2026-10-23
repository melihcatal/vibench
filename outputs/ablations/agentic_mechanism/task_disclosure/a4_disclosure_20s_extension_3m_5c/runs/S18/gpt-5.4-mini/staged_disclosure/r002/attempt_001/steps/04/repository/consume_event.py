import os
from google.cloud import pubsub_v1


def main():
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    subscription_id = os.environ["PUBSUB_SUBSCRIPTION_ID"]
    subscription_path = pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)
    client = pubsub_v1.SubscriberClient()
    response = client.pull(request={"subscription": subscription_path, "max_messages": 1}, timeout=30)
    if not response.received_messages:
        return
    received = response.received_messages[0]
    print(received.message.data.decode("utf-8", errors="replace"))
    client.acknowledge(request={"subscription": subscription_path, "ack_ids": [received.ack_id]})


if __name__ == "__main__":
    main()
