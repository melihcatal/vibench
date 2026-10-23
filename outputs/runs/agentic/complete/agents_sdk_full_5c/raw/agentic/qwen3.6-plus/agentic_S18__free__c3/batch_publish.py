"""Publish a batch of messages with IDs or attributes to Google Cloud Pub/Sub.

Uses Google Cloud Pub/Sub as the concrete external provider.
"""

from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, encode_message, build_attributes
from messaging_models import EventMessage, MessageResponse, BatchMessage


def batch_publish(
    batch: BatchMessage,
    topic_path: Optional[str] = None,
    project: Optional[str] = None,
    topic_name: Optional[str] = None,
) -> List[MessageResponse]:
    """Publish a BatchMessage containing multiple EventMessages to Google Cloud Pub/Sub.

    Args:
        batch: The BatchMessage with messages to publish.
        topic_path: Optional fully-qualified topic path.
        project: Optional GCP project ID override.
        topic_name: Optional topic name override.

    Returns:
        List of MessageResponse, one per published message.
    """
    publisher = get_publisher_client()
    topic = topic_path or get_topic_path(project=project, topic_name=topic_name)

    results: List[MessageResponse] = []
    futures: List[Any] = []

    for event in batch.messages:
        try:
            message_data = event.to_dict()
            encoded_data = encode_message(message_data)

            attrs = build_attributes({
                "event_type": event.event_type,
                "event_id": event.event_id,
                "source": event.source,
                "batch_id": batch.batch_id,
            })

            future = publisher.publish(topic, encoded_data, **attrs)
            futures.append((future, event))
        except Exception as exc:
            results.append(MessageResponse(
                success=False,
                event_id=event.event_id,
                error=str(exc),
                details={"batch_id": batch.batch_id},
            ))

    for future, event in futures:
        try:
            message_id = future.result()
            results.append(MessageResponse(
                success=True,
                message_id=message_id,
                event_id=event.event_id,
                details={"batch_id": batch.batch_id, "topic": topic},
            ))
        except Exception as exc:
            results.append(MessageResponse(
                success=False,
                event_id=event.event_id,
                error=str(exc),
                details={"batch_id": batch.batch_id},
            ))

    return results


def publish_messages_list(
    messages: List[Dict[str, Any]],
    topic_path: Optional[str] = None,
    project: Optional[str] = None,
    topic_name: Optional[str] = None,
) -> List[MessageResponse]:
    """Publish a list of message dictionaries to Google Cloud Pub/Sub.

    Args:
        messages: List of message dicts with event_type, payload, etc.
        topic_path: Optional fully-qualified topic path.
        project: Optional GCP project ID override.
        topic_name: Optional topic name override.

    Returns:
        List of MessageResponse, one per published message.
    """
    batch = BatchMessage()
    for msg in messages:
        event = EventMessage(
            event_type=msg.get("event_type", "unknown"),
            payload=msg.get("payload", {}),
            source=msg.get("source", "default"),
            event_id=msg.get("event_id"),
            attributes=msg.get("attributes", {}),
        )
        batch.add_message(event)

    return batch_publish(batch, topic_path=topic_path, project=project, topic_name=topic_name)
