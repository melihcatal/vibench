"""
Consumes one message from a managed subscription.

Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Interface: SDK
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import json
from typing import Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError

from messaging_client import MessagingConfig, PubSubClientHelper
from messaging_models import EventMessage, ConsumeResponse


def consume_event(
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
    timeout: float = 10.0,
) -> ConsumeResponse:
    """
    Consume one message from a Google Cloud Pub/Sub subscription.

    Args:
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.
        timeout: Timeout in seconds for waiting for a message.

    Returns:
        ConsumeResponse with the consumed message or error.
    """
    cfg = config or MessagingConfig()
    helper = client or PubSubClientHelper(config=cfg)

    try:
        response = helper.subscriber.pull(
            request={
                "subscription": cfg.subscription_path,
                "max_messages": 1,
            },
            timeout=timeout,
        )

        if not response.received_messages:
            return ConsumeResponse(
                success=True,
                message=None,
                error="No messages available",
            )

        received = response.received_messages[0]
        pubsub_message = received.message

        data = pubsub_message.data.decode("utf-8")
        attributes = dict(pubsub_message.attributes)

        event_message = EventMessage.from_json(data)
        event_message.attributes.update(
            {k: v for k, v in attributes.items() if k not in event_message.attributes}
        )

        ack_id = received.ack_id
        helper.subscriber.acknowledge(
            request={
                "subscription": cfg.subscription_path,
                "ack_ids": [ack_id],
            }
        )

        return ConsumeResponse(
            success=True,
            message=event_message,
            raw_message=received,
        )

    except GoogleAPIError as e:
        return ConsumeResponse(
            success=False,
            error=f"Google Cloud Pub/Sub API error: {str(e)}",
        )
    except Exception as e:
        return ConsumeResponse(
            success=False,
            error=f"Failed to consume message: {str(e)}",
        )


def consume_with_nack(
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
    timeout: float = 10.0,
) -> ConsumeResponse:
    """
    Consume a message without acknowledging (for inspection before processing).

    Args:
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.
        timeout: Timeout in seconds for waiting for a message.

    Returns:
        ConsumeResponse with the consumed message.
    """
    cfg = config or MessagingConfig()
    helper = client or PubSubClientHelper(config=cfg)

    try:
        response = helper.subscriber.pull(
            request={
                "subscription": cfg.subscription_path,
                "max_messages": 1,
            },
            timeout=timeout,
        )

        if not response.received_messages:
            return ConsumeResponse(
                success=True,
                message=None,
                error="No messages available",
            )

        received = response.received_messages[0]
        pubsub_message = received.message

        data = pubsub_message.data.decode("utf-8")
        event_message = EventMessage.from_json(data)

        return ConsumeResponse(
            success=True,
            message=event_message,
            raw_message=received,
        )

    except GoogleAPIError as e:
        return ConsumeResponse(
            success=False,
            error=f"Google Cloud Pub/Sub API error: {str(e)}",
        )
    except Exception as e:
        return ConsumeResponse(
            success=False,
            error=f"Failed to consume message: {str(e)}",
        )
