"""publish_event.py - Publishes a JSON event to a Google Cloud Pub/Sub topic."""

import json
import logging
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError
from messaging_client import get_pubsub_publisher_client, PUBSUB_TOPIC_ID, PUBSUB_PROJECT_ID
from messaging_models import PubSubPublishRequest, PubSubPublishResponse

logger = logging.getLogger(__name__)


def publish_event(event_data: dict, event_id: str = None) -> PubSubPublishResponse:
    """Publish a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event_data: Dictionary containing the event payload.
        event_id: Optional unique event identifier.

    Returns:
        PubSubPublishResponse with message_id and status.
    """
    request = PubSubPublishRequest(
        topic_id=PUBSUB_TOPIC_ID,
        project_id=PUBSUB_PROJECT_ID,
        event_data=event_data,
        event_id=event_id,
    )

    publisher = get_pubsub_publisher_client()

    attributes = {
        "event_type": event_data.get("event_type", "unknown"),
        "content_type": "application/json",
    }
    if request.event_id:
        attributes["event_id"] = request.event_id

    payload = json.dumps(request.event_data).encode("utf-8")

    try:
        future = publisher.publish(
            request.full_topic_name(),
            payload,
            **attributes,
        )
        message_id = future.result(timeout=30)
        logger.info(
            "Published event to %s with message_id=%s",
            request.full_topic_name(),
            message_id,
        )
        return PubSubPublishResponse(
            message_id=message_id,
            status="published",
            topic_name=request.full_topic_name(),
        )
    except GoogleAPIError as exc:
        logger.error("Failed to publish event to Pub/Sub: %s", exc)
        return PubSubPublishResponse(
            message_id=None,
            status="failed",
            topic_name=request.full_topic_name(),
            error=str(exc),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_event = {
        "event_type": "user_signup",
        "user_id": "usr_9923",
        "email": "test@example.com",
        "timestamp": "2024-01-15T10:30:00Z",
    }
    response = publish_event(event_data=sample_event, event_id="evt_001")
    print(f"Publish result: {response}")
