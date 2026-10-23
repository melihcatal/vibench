import json
import os
from typing import Any, Dict, List, Optional

from google.cloud import pubsub_v1

from messaging_client import get_publisher
from messaging_models import BatchPublishRequest, build_event_payload


def batch_publish(request: Optional[BatchPublishRequest] = None, **kwargs: Any) -> Dict[str, Any]:
    if request is None:
        request = BatchPublishRequest.from_kwargs(**kwargs)
    publisher = get_publisher()
    topic_path = publisher.topic_path(request.project_id, request.topic_id)
    results: List[Dict[str, Any]] = []
    for item in request.messages:
        payload = build_event_payload(item.data, item.attributes)
        future = publisher.publish(topic_path, payload, message_id=item.message_id, **item.attributes)
        results.append({"message_id": future.result(timeout=request.timeout_seconds), "item_id": item.message_id})
    return {"results": results, "topic_path": topic_path, "provider": "google_pubsub"}


def main() -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    topic_id = os.environ.get("PUBSUB_TOPIC", "")
    request = BatchPublishRequest(project_id=project_id, topic_id=topic_id, messages=[])
    print(json.dumps(batch_publish(request), sort_keys=True))


if __name__ == "__main__":
    main()
