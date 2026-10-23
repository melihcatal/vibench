from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from translation_models import UnsafeCopyResult, normalize_text_list

PROVIDER_NAME = "OpenAI"
MODEL_ID = "gpt-4o-mini"


def check_unsafe_copy(copy_segments: Iterable[str]) -> UnsafeCopyResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = normalize_text_list(copy_segments)
    prompt = "Flag unsafe or policy-risky localized copy and explain briefly: " + " | ".join(normalized)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You detect unsafe marketing or localized copy."},
            {"role": "user", "content": prompt},
        ],
    )
    content = (response.choices[0].message.content or "").lower()
    reasons: List[str] = [line.strip("-• \t") for line in content.splitlines() if line.strip()]
    unsafe = any(keyword in content for keyword in ("unsafe", "harm", "disallowed", "risk"))
    return UnsafeCopyResult(provider=PROVIDER_NAME, unsafe=unsafe, reasons=reasons)
