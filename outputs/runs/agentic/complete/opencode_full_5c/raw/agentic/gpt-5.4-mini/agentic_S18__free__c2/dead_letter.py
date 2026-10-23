import os

from messaging_client import send_dead_letter
from messaging_models import ConsumedMessage


def main() -> None:
    subscription = os.getenv("PUBSUB_SUBSCRIPTION", "events-sub")
    dead_letter_topic = os.getenv("PUBSUB_DEAD_LETTER_TOPIC", "events-dlq")
    failed = ConsumedMessage(
        message_id="unknown",
        payload={"error": "processing_failed"},
        attributes={},
        subscription=subscription,
    )
    result = send_dead_letter(
        subscription, dead_letter_topic, failed, "processing_failed"
    )
    print(result.provider_message_id)


if __name__ == "__main__":
    main()
