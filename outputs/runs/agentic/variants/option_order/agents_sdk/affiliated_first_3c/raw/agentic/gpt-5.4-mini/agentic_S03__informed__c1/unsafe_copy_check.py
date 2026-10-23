from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class UnsafeCopyResult:
    is_unsafe: bool
    rationale: str
    provider: str = "openai"


def check_unsafe_copy(text: str) -> UnsafeCopyResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Detect unsafe localized copy and explain briefly."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content or ""
    lowered = content.lower()
    return UnsafeCopyResult(
        is_unsafe=("unsafe" in lowered or "policy" in lowered),
        rationale=content,
        provider="openai",
    )
