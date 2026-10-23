import os
from typing import Dict

import requests


PERSPECTIVE_HOST = "commentanalyzer.googleapis.com"


def check_live_transcript_text(text: str) -> Dict[str, object]:
    key = os.environ["PERSPECTIVE_API_KEY"]
    url = f"https://{PERSPECTIVE_HOST}/v1alpha1/comments:analyze?key={key}"
    payload = {
        "comment": {"text": text},
        "languages": [os.getenv("PERSPECTIVE_LANGUAGE", "en")],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
