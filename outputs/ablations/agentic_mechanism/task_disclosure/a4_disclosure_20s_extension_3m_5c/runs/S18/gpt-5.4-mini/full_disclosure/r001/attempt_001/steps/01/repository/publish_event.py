import json
import os
from typing import Any, Dict, Optional

import requests


def publish_event(event: Dict[str, Any], topic: Optional[str] = None) -> Dict[str, Any]:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = topic or os.environ["PUBSUB_TOPIC"]
    access_token = os.environ["GOOGLE_OAUTH_ACCESS_TOKEN"]
    url = f"https://pubsub.googleapis.com/v1/projects/{project_id}/topics/{topic_id}:publish"
    payload = {
        "messages": [
            {
                "data": json.dumps(event, separators=(",", ":")).encode("utf-8").decode("latin1")
            }
        ]
    }
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
