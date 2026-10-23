import os
from typing import Any, Dict

from openai import OpenAI


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories)}
