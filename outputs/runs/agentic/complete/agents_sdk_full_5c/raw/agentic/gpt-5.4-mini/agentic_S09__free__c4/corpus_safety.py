import os
from typing import Iterable

from openai import OpenAI

OPENAI_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "omni-moderation-latest")


def corpus_safety(texts: Iterable[str]) -> dict[str, object]:
    client = OpenAI()
    joined = list(texts)
    moderation = client.moderations.create(model=OPENAI_SAFETY_MODEL, input=joined)
    return {
        "provider": "openai",
        "model": OPENAI_SAFETY_MODEL,
        "flagged": any(result.flagged for result in moderation.results),
        "results": [result.model_dump() for result in moderation.results],
    }
