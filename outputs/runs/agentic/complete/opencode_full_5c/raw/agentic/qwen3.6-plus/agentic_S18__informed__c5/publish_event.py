from messaging_models import EventMessage, PublishResult, normalize_event_payload
from messaging_client import publish_message_to_topic, ensure_topic_exists


def publish_event(
    topic_name: str,
    event_type: str,
    payload: dict,
    source: str = "",
    attributes: dict = None,
) -> PublishResult:
    normalized_payload = normalize_event_payload(payload)
    event = EventMessage(
        event_type=event_type,
        source=source,
        payload=normalized_payload,
        attributes=attributes or {},
    )
    ensure_topic_exists(topic_name)
    try:
        message_id = publish_message_to_topic(topic_name, event, attributes)
        return PublishResult(
            message_id=message_id,
            success=True,
            topic=topic_name,
        )
    except Exception as e:
        return PublishResult(
            success=False,
            error=str(e),
            topic=topic_name,
        )


if __name__ == "__main__":
    result = publish_event(
        topic_name="events-topic",
        event_type="user.created",
        payload={"user_id": "12345", "email": "user@example.com"},
        source="auth-service",
        attributes={"priority": "high"},
    )
    print(result.to_dict())
