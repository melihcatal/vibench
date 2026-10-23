from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic


ANTHROPIC_MODEL = os.getenv("ANTHROPIC_SAFETY_MODEL", "claude-3-5-haiku-latest")


def check_text_safety(text_fields: Iterable[str]) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    joined_text = "\n".join(text_fields)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=220,
        system="You review user-generated content and classify unsafe material, returning concise findings.",
        messages=[
            {"role": "user", "content": f"Assess the following document fields for safety risks and policy concerns:\n{joined_text}"}
        ],
    )
    return "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
