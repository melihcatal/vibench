import os

from messaging_client import publish_message
from messaging_models import MessageRequest


def main() -> None:
    topic = os.getenv("PUBSUB_TOPIC", "events")
    payload = {
        "event_type": "customer.created",
        "customer_id": os.getenv("CUSTOMER_ID", "cust_001"),
    }
    result = publish_message(
        MessageRequest(
            topic=topic, payload=payload, attributes={"source": "publish_event"}
        )
    )
    print(result.provider_message_id)


if __name__ == "__main__":
    main()
