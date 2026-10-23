import json
import os
import uuid
from typing import List, Dict
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import BatchPublishRequest, BatchPublishResponse, PublishResponse


def batch_publish(
    events: List[Dict], event_type: str = "batch", default_attributes: Dict = None
) -> BatchPublishResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    request = BatchPublishRequest(
        events=events,
        event_type=event_type,
        default_attributes=default_attributes or {},
    )

    published_results = []
    failed_results = []

    for idx, event_data in enumerate(request.events):
        event_id = event_data.get("id", str(uuid.uuid4()))
        payload = json.dumps(event_data).encode("utf-8")

        attrs = {
            "event_type": request.event_type,
            "event_id": event_id,
            "batch_index": str(idx),
            "content_type": "application/json",
        }
        attrs.update(request.default_attributes)

        if "attributes" in event_data and isinstance(event_data["attributes"], dict):
            attrs.update(event_data["attributes"])

        try:
            future = publisher.publish(topic_path, data=payload, **attrs)
            message_id = future.result()
            published_results.append(
                PublishResponse(
                    message_id=message_id,
                    topic_path=topic_path,
                    status="published",
                    event_type=request.event_type,
                    event_id=event_id,
                )
            )
        except Exception as e:
            failed_results.append(
                {"event_id": event_id, "error": str(e), "status": "failed"}
            )

    return BatchPublishResponse(
        published=published_results,
        failed=failed_results,
        total_requested=len(request.events),
        topic_path=topic_path,
    )


if __name__ == "__main__":
    sample_events = [
        {"id": "evt_001", "user_id": "u1", "action": "login"},
        {"id": "evt_002", "user_id": "u2", "action": "purchase", "amount": 29.99},
        {"id": "evt_003", "user_id": "u3", "action": "logout"},
    ]
    response = batch_publish(sample_events, event_type="user.activity")
    print(json.dumps(response.to_dict(), indent=2, default=str))
