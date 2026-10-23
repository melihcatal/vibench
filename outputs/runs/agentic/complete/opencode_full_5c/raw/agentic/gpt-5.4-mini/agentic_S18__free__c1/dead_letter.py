from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import normalize_payload


def dead_letter(topic: str, failed_payload: object, reason: str) -> str:
    client = publisher_client()
    data = normalize_payload(failed_payload)
    data["dead_letter_reason"] = reason
    future = client.publish(topic_path(topic), encode_json(data), reason=reason)
    return future.result()
