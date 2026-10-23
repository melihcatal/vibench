from typing import Any, Dict

from openai import OpenAI


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": bool(result.flagged), "provider": "openai", "model": "omni-moderation-latest"}
