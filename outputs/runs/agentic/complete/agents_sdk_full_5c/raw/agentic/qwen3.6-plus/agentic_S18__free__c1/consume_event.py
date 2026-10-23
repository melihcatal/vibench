"""consume_event.py - Consumes one message from a Google Cloud Pub/Sub subscription."""

import json
import logging
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message
from google.api_core.exceptions import GoogleAPIError
from messaging_client import get_pubsub_subscriber_client, PUBSUB_SUBSCRIPTION_ID, PUBSUB_PROJECT_ID
from messaging_models import PubSubConsumeResponse

logger = logging.getLogger(__name__)


def consume_event(acknowledge: bool = True, timeout: float = 10.0) -> PubSubConsumeResponse:
    """Consume a single message from a Google Cloud Pub/Sub subscription.

    Args:
        acknowledge: Whether to acknowledge the message after consumption.
        timeout: Maximum seconds to wait for a message.

    Returns:
        PubSubConsumeResponse containing message data or None.
    """
    subscriber = get_pubsub_subscriber_client()
    subscription_path = subscriber.subscription_path(
        PUBSUB_PROJECT_ID, PUBSUB_SUBSCRIPTION_ID
    )

    try:
        with pubsub_v1.SubscriberClient() as sub_client:
            response = sub_client.pull(
                subscription=subscription_path,
                max_messages=1,
                timeout=timeout,
            )

            if not response.received_messages:
                logger.info("No messages received on %s", subscription_path)
                return PubSubConsumeResponse(
                    message_id=None,
                    payload=None,
                    attributes={},
                    status="no_message",
                )

            received = response.received_messages[0]
            message = received.message
            message_id = message.message_id

            data = json.loads(message.data.decode("utf-8")) if message.data else None
            attributes = dict(message.attributes)

            logger.info(
                "Consumed message_id=%s from %s",
                message_id,
                subscription_path,
            )

            if acknowledge:
                sub_client.acknowledge(
                    subscription=subscription_path,
                    ack_ids=[received.ack_id],
                )

            return PubSubConsumeResponse(
                message_id=message_id,
                payload=data,
                attributes=attributes,
                status="consumed",
            )

    except GoogleAPIError as exc:
        logger.error("Failed to consume message from Pub/Sub: %s", exc)
        return PubSubConsumeResponse(
            message_id=None,
            payload=None,
            attributes={},
            status="failed",
            error=str(exc),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = consume_event(acknowledge=False)
    print(f"Consume result: {result}")
