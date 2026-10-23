import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_publisher
from messaging_models import DeadLetterRequest, build_event_payload


def dead_letter(request: Optional[DeadLetterRequest] = None, **kwargs: Any) -> Dict[str, Any]:
    if request is None:
        request = DeadLetterRequest.from_kwargs(**kwargs)
    publisher = get_publisher()
    topic_path = publisher.topic_path(request.project_id, request.dead_letter_topic_id)
    payload = build_event_payload(request.data, request.attributes)
    future = publisher.publish(topic_path, payload, reason=request.reason, **request.attributes)
    message_id = future.result(timeout=request.timeout_seconds)
    return {"message_id": message_id, "topic_path": topic_path, "provider": "google_pubsub"}


def main() -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    dead_letter_topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "")
    request = DeadLetterRequest(project_id=project_id, dead_letter_topic_id=dead_letter_topic_id, reason="processing_failed", data={"event": "dead_letter"})
    print(json.dumps(dead_letter(request), sort_keys=True))


if __name__ == "__main__":
    main()
