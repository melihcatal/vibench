import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_publisher
from messaging_models import PublishRequest, build_event_payload


def publish_event(request: Optional[PublishRequest] = None, **kwargs: Any) -> Dict[str, Any]:
    if request is None:
        request = PublishRequest.from_kwargs(**kwargs)
    publisher = get_publisher()
    topic_path = publisher.topic_path(request.project_id, request.topic_id)
    payload = build_event_payload(request.data, request.attributes)
    future = publisher.publish(topic_path, payload, **request.attributes)
    message_id = future.result(timeout=request.timeout_seconds)
    return {"message_id": message_id, "topic_path": topic_path, "provider": "google_pubsub"}


def main() -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    topic_id = os.environ.get("PUBSUB_TOPIC", "")
    request = PublishRequest(project_id=project_id, topic_id=topic_id, data={"event": "created"})
    print(json.dumps(publish_event(request), sort_keys=True))


if __name__ == "__main__":
    main()
