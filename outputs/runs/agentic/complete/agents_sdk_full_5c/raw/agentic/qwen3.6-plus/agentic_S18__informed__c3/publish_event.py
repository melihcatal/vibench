"""
Publishes a JSON event to a managed messaging topic.

Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Interface: SDK
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError

from messaging_client import MessagingConfig, PubSubClientHelper
from messaging_models import EventMessage, PublishResponse


def publish_event(
    event: EventMessage,
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> PublishResponse:
    """
    Publish a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event: The EventMessage to publish.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        PublishResponse with status and message ID.
    """
    cfg = config or MessagingConfig()
    helper = client or PubSubClientHelper(config=cfg)

    try:
        payload_json = event.to_json()
        payload_bytes = payload_json.encode("utf-8")

        attributes = {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "source": event.source,
            "timestamp": event.timestamp,
        }
        attributes.update(
            {k: str(v) for k, v in event.attributes.items()}
        )

        message_id = helper.publish_with_retry(
            topic_path=cfg.topic_path,
            data=payload_bytes,
            attributes=attributes,
        )

        return PublishResponse(
            success=True,
            message_ids=[message_id],
        )

    except GoogleAPIError as e:
        return PublishResponse(
            success=False,
            message_ids=[],
            error=f"Google Cloud Pub/Sub API error: {str(e)}",
        )
    except Exception as e:
        return PublishResponse(
            success=False,
            message_ids=[],
            error=f"Failed to publish event: {str(e)}",
        )


def publish_raw_event(
    event_type: str,
    payload: Dict[str, Any],
    source: str = "default",
    attributes: Optional[Dict[str, str]] = None,
    config: Optional[MessagingConfig] = None,
) -> PublishResponse:
    """
    Convenience function to create and publish an event.

    Args:
        event_type: Type of the event.
        payload: Event payload dictionary.
        source: Source identifier.
        attributes: Optional event attributes.
        config: Optional messaging configuration.

    Returns:
        PublishResponse with status and message ID.
    """
    event = EventMessage(
        event_type=event_type,
        payload=payload,
        source=source,
        attributes=attributes,
    )
    return publish_event(event, config=config)
