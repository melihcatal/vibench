from typing import Any, Dict

from openai import OpenAI


def check_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest", input=str(record)
    )
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump()}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return check_text_safety(event["record"])
