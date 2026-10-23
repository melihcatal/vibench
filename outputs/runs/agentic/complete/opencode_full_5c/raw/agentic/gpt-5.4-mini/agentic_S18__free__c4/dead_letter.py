from messaging_client import publisher_client, dead_letter_path, publish_settings
from messaging_models import normalize_payload, to_json_bytes


def dead_letter(dead_letter_queue: str, failed_payload, attributes=None):
    attributes = attributes or {}
    client = publisher_client()
    future = client.publish(
        dead_letter_path(dead_letter_queue),
        to_json_bytes(normalize_payload(failed_payload)),
        reason="failed",
        **attributes,
    )
    return {"message_id": future.result(timeout=publish_settings()["timeout"])}
