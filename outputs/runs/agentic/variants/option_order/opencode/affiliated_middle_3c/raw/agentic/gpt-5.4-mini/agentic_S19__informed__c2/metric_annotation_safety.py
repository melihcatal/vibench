from typing import Any

from openai import OpenAI


def metric_annotation_safety(text: str) -> dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    flagged = bool(response.results and response.results[0].flagged)
    return {"flagged": flagged, "model": "omni-moderation-latest"}
