import os

from messaging_client import publish_batch
from messaging_models import MessageBatchItem


def main() -> None:
    topic = os.getenv("PUBSUB_TOPIC", "events")
    items = [
        MessageBatchItem(
            data={"event_type": "order.created", "order_id": "ord_001"},
            attributes={"batch_id": "b1"},
        ),
        MessageBatchItem(
            data={"event_type": "order.shipped", "order_id": "ord_002"},
            attributes={"batch_id": "b1"},
        ),
    ]
    result = publish_batch(topic, items)
    print(result.message_ids)


if __name__ == "__main__":
    main()
