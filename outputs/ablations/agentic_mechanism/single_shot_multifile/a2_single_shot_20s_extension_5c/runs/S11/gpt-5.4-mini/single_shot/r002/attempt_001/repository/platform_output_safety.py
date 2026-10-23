from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client

SAFETY_MODEL = "omni-moderation-latest"


def check_platform_output_safety(text: str, client: OpenAI | None = None) -> Dict[str, Any]:
    api_client = client or get_openai_client()
    result = api_client.moderations.create(model=SAFETY_MODEL, input=text)
    first = result.results[0] if getattr(result, "results", None) else None
    return {"provider": "openai", "model": SAFETY_MODEL, "flagged": getattr(first, "flagged", False), "raw": result}
