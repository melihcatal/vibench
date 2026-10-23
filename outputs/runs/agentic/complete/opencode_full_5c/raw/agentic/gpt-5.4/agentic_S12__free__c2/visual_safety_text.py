from __future__ import annotations

import json
import os
from typing import Iterable, List

import requests


OPENAI_MODERATIONS_API_URL = "https://api.openai.com/v1/moderations"


def visual_safety_text(labels: Iterable[str]) -> List[dict]:
    api_key = os.environ["OPENAI_API_KEY"]
    joined = ", ".join(label.strip() for label in labels if label and label.strip())
    response = requests.post(
        OPENAI_MODERATIONS_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": "omni-moderation-latest", "input": joined}),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])
