from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_openai_client


def moderate_transcript(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return result.model_dump() if hasattr(result, "model_dump") else result.dict()
