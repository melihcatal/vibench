import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher, topic_path
from messaging_models import DeadLetterRequest, normalize_payload


def send_dead_letter(request: DeadLetterRequest) -> str:
    publisher = get_publisher()
    destination = topic_path(request.destination)
    payload = {
        "original_message_id": request.original_message_id,
        "payload": request.payload,
        "error": request.error,
    }
    future = publisher.publish(
        destination, data=normalize_payload(payload), dead_letter="true"
    )
    return future.result()


def main() -> None:
    req = DeadLetterRequest(
        destination="dead-letter",
        original_message_id="1",
        payload={"type": "failed"},
        error="processing failed",
    )
    print(json.dumps({"message_id": send_dead_letter(req)}))


if __name__ == "__main__":
    main()
