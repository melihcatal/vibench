from typing import Any, Dict

import requests

from identity_models import normalize_text


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": normalize_text(profile_text)},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        url, params={"key": "${PERSPECTIVE_API_KEY}"}, json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return {"approved": True, "analysis": data}
