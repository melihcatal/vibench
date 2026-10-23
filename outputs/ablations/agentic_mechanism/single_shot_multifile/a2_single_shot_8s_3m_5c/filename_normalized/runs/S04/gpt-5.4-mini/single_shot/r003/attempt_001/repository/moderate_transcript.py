from __future__ import annotations

from typing import Any, Dict, Iterable

from speech_client import load_config
from openai import OpenAI


def moderate_transcript(text: str, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    config = load_config()
    client = OpenAI(api_key=config.api_key)
    result = client.moderations.create(model=model, input=text)
    return {"model": model, "flagged": result.results[0].flagged, "categories": result.results[0].categories.model_dump()}
