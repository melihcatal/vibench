"""
Sends failed messages to a dead-letter destination.

Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Interface: SDK
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError

from messaging_client import MessagingConfig, PubSubClientHelper
from messaging_models import EventMessage, DeadLetterResponse, normalize_payload


def send_to_dead_letter(
    original_message: EventMessage,
    failure_reason: str,
    original_message_id: Optional[str] = None,
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> DeadLetterResponse:
    """
    Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_message: The original EventMessage that failed processing.
        failure_reason: Description of why the message failed.
        original_message_id: The original Pub/Sub message ID if available.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        DeadLetterResponse with status and dead-letter message ID.
    """
    cfg = config or MessagingConfig()
    helper = client or PubSubClientHelper(config=cfg)

    dead_letter_payload = {
        "original_event": original_message.to_dict(),
        "failure_reason": failure_reason,
        "original_message_id": original_message_id,
        "dead_lettered_at": datetime.now(timezone.utc).isoformat(),
        "original_event_type": original_message.event_type,
        "original_source": original_message.source,
    }

    try:
        payload_json = json.dumps(dead_letter_payload, default=str)
        payload_bytes = payload_json.encode("utf-8")

        attributes = {
            "event_type": "dead_letter",
            "original_event_type": original_message.event_type,
            "original_event_id": original_message.event_id,
            "failure_reason": failure_reason,
            "dead_letter_source": "messaging_service",
        }

        message_id = helper.publish_with_retry(
            topic_path=cfg.dead_letter_topic_path,
            data=payload_bytes,
            attributes=attributes,
        )

        return DeadLetterResponse(
            success=True,
            dead_letter_id=message_id,
            original_message_id=original_message_id or original_message.event_id,
        )

    except GoogleAPIError as e:
        return DeadLetterResponse(
            success=False,
            original_message_id=original_message_id or original_message.event_id,
            error=f"Google Cloud Pub/Sub API error: {str(e)}",
        )
    except Exception as e:
        return DeadLetterResponse(
            success=False,
            original_message_id=original_message_id or original_message.event_id,
            error=f"Failed to send to dead-letter: {str(e)}",
        )


def dead_letter_from_raw(
    raw_message_data: bytes,
    raw_attributes: Dict[str, str],
    failure_reason: str,
    message_id: Optional[str] = None,
    config: Optional[MessagingConfig] = None,
) -> DeadLetterResponse:
    """
    Create a dead-letter entry from raw message data.

    Args:
        raw_message_data: Raw bytes of the original message.
        raw_attributes: Original message attributes.
        failure_reason: Description of why the message failed.
        message_id: Original Pub/Sub message ID.
        config: Optional messaging configuration.

    Returns:
        DeadLetterResponse with status and dead-letter message ID.
    """
    try:
        data_str = raw_message_data.decode("utf-8")
        event_message = EventMessage.from_json(data_str)
    except (json.JSONDecodeError, UnicodeDecodeError):
        event_message = EventMessage(
            event_type="unknown",
            payload=normalize_payload(raw_message_data.decode("utf-8", errors="replace")),
            source="unknown",
        )

    return send_to_dead_letter(
        original_message=event_message,
        failure_reason=failure_reason,
        original_message_id=message_id,
        config=config,
    )


def configure_dead_letter_policy(
    subscription_path: str,
    dead_letter_topic_path: str,
    max_delivery_attempts: int = 5,
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> bool:
    """
    Configure a dead-letter policy on an existing subscription.

    Args:
        subscription_path: Full path to the subscription.
        dead_letter_topic_path: Full path to the dead-letter topic.
        max_delivery_attempts: Maximum delivery attempts before dead-lettering.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        True if policy was configured successfully.
    """
    helper = client or PubSubClientHelper(config=config)
    subscriber = helper.subscriber

    try:
        policy = helper.build_dead_letter_policy(
            dead_letter_topic_path=dead_letter_topic_path,
            max_delivery_attempts=max_delivery_attempts,
        )

        subscription = subscriber.get_subscription(
            request={"subscription": subscription_path}
        )
        subscription.dead_letter_policy = policy

        subscriber.update_subscription(
            request={
                "subscription": subscription,
                "update_mask": {"paths": ["dead_letter_policy"]},
            }
        )
        return True

    except GoogleAPIError:
        return False
