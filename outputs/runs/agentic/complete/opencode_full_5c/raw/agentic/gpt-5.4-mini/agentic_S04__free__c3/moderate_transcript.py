from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_client


def moderate_transcript(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client: OpenAI = get_client()
    text = "\n".join(segment.get("text", "") for segment in segments)
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    return result.model_dump()
