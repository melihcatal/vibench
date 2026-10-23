from __future__ import annotations

import os

from openai import OpenAI

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_corpus_text(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    return not result.results[0].flagged
