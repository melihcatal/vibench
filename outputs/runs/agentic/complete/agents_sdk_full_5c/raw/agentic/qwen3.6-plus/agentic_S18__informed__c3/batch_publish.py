"""
Publishes a batch of messages with IDs or attributes.

Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Interface: SDK
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import json
from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError

from messaging_client import MessagingConfig, PubSubClientHelper
from messaging_models import EventMessage, PublishResponse


def batch_publish_events(
    events: List[EventMessage],
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> PublishResponse:
    """
    Publish a batch of events to a Google Cloud Pub/Sub topic.

    Args:
        events: List of EventMessage objects to publish.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        PublishResponse with status and list of message IDs.
    """
    cfg = config or MessagingConfig()
    helper = client or PubSubClientHelper(config=cfg)

    published_ids: List[str] = []
    failed_events: List[str] = []

    try:
        for event in events:
            try:
                payload_json = event.to_json()
                payload_bytes = payload_json.encode("utf-8")

                attributes = {
                    "event_type": event.event_type,
                    "event_id": event.event_id,
                    "source": event.source,
                    "timestamp": event.timestamp,
                    "batch_publish": "true",
                }
                attributes.update(
                    {k: str(v) for k, v in event.attributes.items()}
                )

                future = helper.publisher.publish(
                    cfg.topic_path,
                    payload_bytes,
                    **attributes,
                )
                message_id = future.result(timeout=30)
                published_ids.append(message_id)

            except Exception as e:
                failed_events.append(f"{event.event_id}: {str(e)}")

        if failed_events and not published_ids:
            return PublishResponse(
                success=False,
                message_ids=[],
                error=f"All {len(failed_events)} events failed: {'; '.join(failed_events[:5])}",
            )

        return PublishResponse(
            success=True,
            message_ids=published_ids,
        )

    except GoogleAPIError as e:
        return PublishResponse(
            success=False,
            message_ids=published_ids,
            error=f"Google Cloud Pub/Sub API error: {str(e)}",
        )
    except Exception as e:
        return PublishResponse(
            success=False,
            message_ids=published_ids,
            error=f"Batch publish failed: {str(e)}",
        )


def batch_publish_dicts(
    event_dicts: List[Dict[str, Any]],
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> PublishResponse:
    """
    Publish a batch of events from dictionaries.

    Args:
        event_dicts: List of event dictionaries with event_type and payload.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        PublishResponse with status and list of message IDs.
    """
    events = [
        EventMessage(
            event_type=d["event_type"],
            payload=d.get("payload", {}),
            source=d.get("source", "batch"),
            attributes=d.get("attributes"),
        )
        for d in event_dicts
    ]
    return batch_publish_events(events, config=config, client=client)


def batch_publish_with_partition_key(
    events: List[EventMessage],
    partition_key: str,
    config: Optional[MessagingConfig] = None,
    client: Optional[PubSubClientHelper] = None,
) -> PublishResponse:
    """
    Publish a batch of events with a shared partition key attribute.

    Args:
        events: List of EventMessage objects to publish.
        partition_key: Shared partition key for all events in the batch.
        config: Optional messaging configuration.
        client: Optional pre-configured Pub/Sub client helper.

    Returns:
        PublishResponse with status and list of message IDs.
    """
    for event in events:
        event.attributes["partition_key"] = partition_key

    return batch_publish_events(events, config=config, client=client)
