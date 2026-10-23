"""Publish a batch of messages with IDs and attributes to Google Cloud Pub/Sub.

Uses the google-cloud-pubsub SDK to publish multiple events in a single
batch call. Authentication relies on GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1

from messaging_client import (
    get_publisher,
    topic_path,
    normalize_payload,
    build_attributes,
)
from messaging_models import (
    PublishRequest,
    PublishResponse,
    BatchPublishRequest,
    BatchPublishResponse,
)


def batch_publish(
    events: List[Dict[str, Any]],
    topic_id: Optional[str] = None,
) -> BatchPublishResponse:
    """Publish a batch of events to a Google Cloud Pub/Sub topic.

    Each event dict must contain at minimum:
        - event_type (str)
        - source (str)
        - payload (dict)
      Optional keys: event_id (str), attributes (dict[str, str]).

    Args:
        events: List of event dictionaries to publish.
        topic_id: Optional topic ID override.

    Returns:
        BatchPublishResponse with per-message results.
    """
    publisher: pubsub_v1.PublisherClient = get_publisher()
    target_topic = topic_path(topic_id)

    message_ids: List[str] = []
    success_count = 0
    failure_count = 0

    for idx, evt in enumerate(events):
        request = PublishRequest(
            event_type=evt["event_type"],
            source=evt["source"],
            payload=evt["payload"],
            event_id=evt.get("event_id"),
        )

        data_bytes = normalize_payload(request.payload)

        attrs = build_attributes(
            event_id=request.event_id,
            event_type=request.event_type,
            source=request.source,
            extra=evt.get("attributes"),
        )

        try:
            future = publisher.publish(target_topic, data_bytes, **attrs)
            mid = future.result()
            message_ids.append(mid)
            success_count += 1
        except Exception:
            failure_count += 1

    return BatchPublishResponse(
        batch_id="",
        message_ids=message_ids,
        success_count=success_count,
        failure_count=failure_count,
    )


def batch_publish_from_request(
    batch_request: BatchPublishRequest,
    topic_id: Optional[str] = None,
) -> BatchPublishResponse:
    """Publish a BatchPublishRequest to Google Cloud Pub/Sub.

    Args:
        batch_request: Pre-built BatchPublishRequest object.
        topic_id: Optional topic ID override.

    Returns:
        BatchPublishResponse carrying the Pub/Sub message IDs.
    """
    raw_events: List[Dict[str, Any]] = []
    for evt in batch_request.events:
        raw_event: Dict[str, Any] = {
            "event_type": evt.event_type,
            "source": evt.source,
            "payload": evt.payload,
            "event_id": evt.event_id,
            "attributes": evt.attributes,
        }
        raw_events.append(raw_event)

    resp = batch_publish(raw_events, topic_id=topic_id)
    resp.batch_id = batch_request.batch_id
    return resp


if __name__ == "__main__":
    events = [
        {"event_type": "order.created", "source": "shop-api", "payload": {"order_id": "O-1"}},
        {"event_type": "order.created", "source": "shop-api", "payload": {"order_id": "O-2"}},
        {"event_type": "inventory.updated", "source": "warehouse", "payload": {"sku": "SKU-42", "qty": 10}},
    ]
    resp = batch_publish(events)
    print(json.dumps({"batch_count": len(resp.message_ids), "success": resp.success_count, "failed": resp.failure_count}))
