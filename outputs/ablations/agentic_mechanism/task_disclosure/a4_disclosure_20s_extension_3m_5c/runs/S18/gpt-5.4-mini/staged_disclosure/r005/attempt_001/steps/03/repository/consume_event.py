import os
import sys

from google.cloud import pubsub_v1


def main() -> int:
    project_id = os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")

    if not project_id or not subscription_id:
        return 1

    subscription_path = pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=10)

    if not response.received_messages:
        return 0

    received_message = response.received_messages[0]
    print(received_message.message.data.decode("utf-8", errors="replace"))
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[received_message.ack_id])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
