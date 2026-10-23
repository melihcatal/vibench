"""
Publish a batch of messages with IDs and attributes to Google Cloud Pub/Sub.

Uses the google-cloud-pubsub SDK to publish multiple messages efficiently
to a managed Pub/Sub topic.
Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
"""

import os
import json
import uuid
from typing import Optional, Sequence

from google.cloud import pubsub_v1

from messaging_models import MessagingEvent, PublishResult, BatchPublishResult
from messaging_client import PubSubClientHelper


def publish_batch(
    topic_id: str,
    events: Sequence[MessagingEvent],
    project_id: Optional[str] = None,
) -> BatchPublishResult:
    """
    Publish a batch of MessagingEvents to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The Pub/Sub topic ID to publish to.
        events: Sequence of MessagingEvent objects to publish.
        project_id: Optional GCP project ID.

    Returns:
        BatchPublishResult with individual results and summary.
    """
    helper = PubSubClientHelper(project_id=project_id)
    topic_path = helper.get_topic_path(topic_id)

    batch_result = BatchPublishResult()

    try:
        for event in events:
            try:
                event_json = event.to_json()
                data = event_json.encode("utf-8")

                attributes = {
                    "event_type": event.event_type,
                    "event_id": event.event_id,
                    "batch_publish": "true",
                    "content_type": "application/json",
                }

                future = helper.publisher.publish(
                    topic_path,
                    data=data,
                    **attributes,
                )

                message_id = future.result()
                batch_result.results.append(
                    PublishResult(success=True, message_id=message_id)
                )
                batch_result.total_sent += 1

            except Exception as e:
                batch_result.results.append(
                    PublishResult(
                        success=False,
                        message_id=event.event_id,
                        error=str(e),
                    )
                )
                batch_result.total_failed += 1

    finally:
        helper.close()

    return batch_result


def publish_batch_raw(
    topic_id: str,
    payloads: Sequence[dict],
    event_type: str = "batch.default",
    project_id: Optional[str] = None,
) -> BatchPublishResult:
    """
    Publish a batch of raw dictionary payloads as events.

    Args:
        topic_id: The Pub/Sub topic ID.
        payloads: Sequence of dictionary payloads.
        event_type: Event type for all messages in the batch.
        project_id: Optional GCP project ID.

    Returns:
        BatchPublishResult with outcomes.
    """
    events = [
        MessagingEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            payload=payload,
        )
        for payload in payloads
    ]
    return publish_batch(topic_id, events, project_id=project_id)


if __name__ == "__main__":
    sample_events = [
        MessagingEvent(
            event_type="user.action",
            payload={"user_id": f"usr_{i}", "action": "login"},
        )
        for i in range(5)
    ]

    topic = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
    result = publish_batch(topic, sample_events)
    print(json.dumps(result.to_dict(), indent=2))
