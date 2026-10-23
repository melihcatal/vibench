import json
import os
import sys

from google.cloud import pubsub_v1


def consume_one_message() -> int:
    subscription_path = os.environ["PUBSUB_SUBSCRIPTION"]
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=30,
    )

    if not response.received_messages:
        print(json.dumps({"message": None}))
        return 0

    received = response.received_messages[0]
    message = received.message
    print(
        json.dumps(
            {
                "message_id": message.message_id,
                "data": message.data.decode("utf-8", errors="replace"),
                "attributes": dict(message.attributes),
                "publish_time": message.publish_time.isoformat() if message.publish_time else None,
            }
        )
    )
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received.ack_id],
        }
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(consume_one_message())
    except KeyError as exc:
        print(f"Missing required environment variable: {exc.args[0]}", file=sys.stderr)
        raise SystemExit(1)
