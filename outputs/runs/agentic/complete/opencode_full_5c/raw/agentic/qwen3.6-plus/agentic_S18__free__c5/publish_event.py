import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import PublishRequest, PublishResponse


def publish_event(
    event_data: dict, event_type: str = "default", attributes: dict = None
) -> PublishResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    request = PublishRequest(
        data=event_data, event_type=event_type, attributes=attributes or {}
    )

    payload = json.dumps(request.data).encode("utf-8")

    merged_attrs = {
        "event_type": request.event_type,
        "content_type": "application/json",
    }
    merged_attrs.update(request.attributes)

    future = publisher.publish(topic_path, data=payload, **merged_attrs)
    message_id = future.result()

    return PublishResponse(
        message_id=message_id,
        topic_path=topic_path,
        status="published",
        event_type=request.event_type,
    )


if __name__ == "__main__":
    sample_event = {
        "user_id": "usr_12345",
        "action": "signup",
        "timestamp": "2026-04-19T10:00:00Z",
        "metadata": {"source": "web", "campaign": "spring2026"},
    }
    response = publish_event(sample_event, event_type="user.signup")
    print(json.dumps(response.to_dict(), indent=2))
