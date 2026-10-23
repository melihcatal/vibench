import json
import os
from typing import Any, Dict, Optional

import requests


class DeadLetterError(RuntimeError):
    pass


def send_to_dead_letter(message: Dict[str, Any], reason: str, destination: Optional[str] = None) -> Dict[str, Any]:
    endpoint = destination or os.getenv("SLACK_WEBHOOK_URL")
    if not endpoint:
        raise DeadLetterError("Missing Slack webhook destination")

    payload = {
        "text": f"Dead-lettered message: {reason}",
        "attachments": [
            {
                "color": "danger",
                "fields": [
                    {"title": "Reason", "value": reason, "short": False},
                    {"title": "Message", "value": json.dumps(message, ensure_ascii=False), "short": False},
                ],
            }
        ],
    }

    response = requests.post(endpoint, json=payload, timeout=10)
    if response.status_code >= 400:
        raise DeadLetterError(f"Slack dead-letter delivery failed: {response.status_code} {response.text}")

    return {"ok": True, "status_code": response.status_code}
