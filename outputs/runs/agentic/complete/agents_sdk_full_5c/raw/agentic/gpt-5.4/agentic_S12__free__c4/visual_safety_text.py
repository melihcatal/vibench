from __future__ import annotations

from typing import Dict, Iterable, List
from urllib.parse import urlencode

from vision_client import GOOGLE_PERSPECTIVE_ENDPOINT, get_env, post_json
from vision_models import compact_text_list


PROVIDER = "google_perspective_api"
MODEL = "TOXICITY"


def visual_safety_text(labels: Iterable[str]) -> Dict[str, object]:
    text = ", ".join(compact_text_list(labels))
    api_key = get_env("PERSPECTIVE_API_KEY")
    url = f"{GOOGLE_PERSPECTIVE_ENDPOINT}?{urlencode({'key': api_key})}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": ["en"],
    }
    response = post_json(url, payload)
    scores: Dict[str, float] = {}
    flagged: List[str] = []
    for name, details in response.get("attributeScores", {}).items():
        value = float(details["summaryScore"]["value"])
        scores[name.lower()] = value
        if value >= 0.7:
            flagged.append(name.lower())
    return {"provider": PROVIDER, "scores": scores, "flagged": flagged, "input_text": text}
