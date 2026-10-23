from typing import Any, Dict

from openai import OpenAI


def profile_moderation(text: str) -> Dict[str, Any]:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    flagged = bool(result.results and result.results[0].flagged)
    return {"flagged": flagged, "raw": result.model_dump()}
