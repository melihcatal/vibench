from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from safety_models import SafetyDecision, normalize_openai_moderation_result


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
OPENAI_AUDIO_VOICE = os.getenv("OPENAI_AUDIO_VOICE", "alloy")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_text_with_openai(text: str) -> SafetyDecision:
    client = get_openai_client()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0].model_dump()
    result["model"] = OPENAI_MODERATION_MODEL
    return normalize_openai_moderation_result(text, result)


def moderate_batch_with_openai(texts: Iterable[str]) -> List[SafetyDecision]:
    items = list(texts)
    if not items:
        return []
    client = get_openai_client()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=items)
    decisions: List[SafetyDecision] = []
    for text, result in zip(items, response.results):
        raw = result.model_dump()
        raw["model"] = OPENAI_MODERATION_MODEL
        decisions.append(normalize_openai_moderation_result(text, raw))
    return decisions
