from typing import Any, Dict

from openai import OpenAI


def check_message_safety(payload_text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=payload_text)
    result = response.results[0]
    return {"unsafe": bool(result.flagged), "categories": dict(result.categories), "provider": "openai"}
