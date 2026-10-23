import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def consume_one_message(subscription_path: Optional[str] = None) -> Dict[str, Any]:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    subscription_id = subscription_path or os.environ["PUBSUB_SUBSCRIPTION"]
    client = pubsub_v1.SubscriberClient()
    if "/" in subscription_id:
        subscription = subscription_id
    else:
        subscription = client.subscription_path(project_id, subscription_id)

    response = client.pull(request={"subscription": subscription, "max_messages": 1})
    if not response.received_messages:
        return {"subscription": subscription, "message": None}

    received = response.received_messages[0]
    ack_id = received.ack_id
    message = received.message
    data = message.data.decode("utf-8") if message.data else ""
    attributes = dict(message.attributes)
    client.acknowledge(request={"subscription": subscription, "ack_ids": [ack_id]})
    return {
        "subscription": subscription,
        "message": {
            "message_id": message.message_id,
            "data": data,
            "attributes": attributes,
            "publish_time": message.publish_time.isoformat() if message.publish_time else None,
        },
    }


def main() -> None:
    result = consume_one_message()
    print(result)


if __name__ == "__main__":
    main()
