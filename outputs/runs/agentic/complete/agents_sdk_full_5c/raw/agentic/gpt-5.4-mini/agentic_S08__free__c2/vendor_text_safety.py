from __future__ import annotations

"""Vendor note safety moderation using OpenAI moderation API."""

import os

from openai import OpenAI

OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def vendor_text_safety(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    return result.model_dump()
