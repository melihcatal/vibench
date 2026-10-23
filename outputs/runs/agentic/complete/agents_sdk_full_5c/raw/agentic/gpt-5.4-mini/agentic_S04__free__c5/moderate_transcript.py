from __future__ import annotations

from typing import Dict, List

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client


def moderate_transcript(text: str) -> Dict[str, object]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    categories = moderation.results[0].categories.model_dump()
    flagged = bool(moderation.results[0].flagged)
    return {"flagged": flagged, "categories": categories, "provider": "openai"}
