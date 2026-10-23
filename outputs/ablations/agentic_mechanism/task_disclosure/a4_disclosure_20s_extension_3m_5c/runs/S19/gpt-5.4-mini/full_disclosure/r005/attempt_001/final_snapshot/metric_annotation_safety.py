import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_metric_annotation_safety(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {"model": "omni-moderation-latest", "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    result = data.get("results", [{}])[0]
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    output = {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": flagged,
        "category_scores": category_scores,
        "raw": data,
    }

    if categories:
        output["selected_categories"] = {name: category_scores.get(name) for name in categories}

    return output
