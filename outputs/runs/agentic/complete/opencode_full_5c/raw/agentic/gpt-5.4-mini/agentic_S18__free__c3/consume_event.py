import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_subscriber
from messaging_models import ConsumeRequest, normalize_message


def consume_event(request: Optional[ConsumeRequest] = None, **kwargs: Any) -> Dict[str, Any]:
    if request is None:
        request = ConsumeRequest.from_kwargs(**kwargs)
    subscriber = get_subscriber()
    subscription_path = subscriber.subscription_path(request.project_id, request.subscription_id)
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=request.timeout_seconds)
    if not response.received_messages:
        return {"messages": [], "subscription_path": subscription_path, "provider": "google_pubsub"}
    received = response.received_messages[0]
    message = normalize_message(received.message)
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[received.ack_id])
    return {"messages": [message], "subscription_path": subscription_path, "provider": "google_pubsub"}


def main() -> None:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION", "")
    request = ConsumeRequest(project_id=project_id, subscription_id=subscription_id)
    print(json.dumps(consume_event(request), sort_keys=True))


if __name__ == "__main__":
    main()
