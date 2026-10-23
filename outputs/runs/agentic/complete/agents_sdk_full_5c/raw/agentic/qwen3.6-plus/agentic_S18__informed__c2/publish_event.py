"""
Publish a JSON event to a Google Cloud Pub/Sub managed messaging topic.

Uses the google-cloud-pubsub SDK to publish events to a configured topic.
Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
"""

import os
import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_models import MessagingEvent, PublishResult
from messaging_client import PubSubClientHelper


def publish_event(
    topic_id: str,
    event: MessagingEvent,
    project_id: Optional[str] = None,
) -> PublishResult:
    """
    Publish a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The Pub/Sub topic ID to publish to.
        event: The MessagingEvent to publish.
        project_id: Optional GCP project ID (falls back to GCP_PROJECT_ID env var).

    Returns:
        PublishResult indicating success or failure with the message ID.
    """
    helper = PubSubClientHelper(project_id=project_id)

    try:
        event_json = event.to_json()
        data = event_json.encode("utf-8")

        attributes = {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "content_type": "application/json",
        }

        message_id = helper.publish_message(
            topic_id=topic_id,
            data=data,
            attributes=attributes,
        )

        return PublishResult(
            success=True,
            message_id=message_id,
        )
    except Exception as e:
        return PublishResult(
            success=False,
            error=str(e),
        )
    finally:
        helper.close()


def publish_event_raw(
    topic_id: str,
    payload: dict,
    event_type: str = "default",
    project_id: Optional[str] = None,
) -> PublishResult:
    """
    Publish a raw dictionary payload as a JSON event to Google Cloud Pub/Sub.

    Args:
        topic_id: The Pub/Sub topic ID.
        payload: Dictionary payload to publish.
        event_type: Event type string for categorization.
        project_id: Optional GCP project ID.

    Returns:
        PublishResult with outcome.
    """
    event = MessagingEvent(
        event_type=event_type,
        payload=payload,
    )
    return publish_event(topic_id, event, project_id=project_id)


if __name__ == "__main__":
    sample_event = MessagingEvent(
        event_type="user.signup",
        payload={"user_id": "usr_12345", "email": "user@example.com"},
    )
    topic = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
    result = publish_event(topic, sample_event)
    print(json.dumps(result.to_dict()))
