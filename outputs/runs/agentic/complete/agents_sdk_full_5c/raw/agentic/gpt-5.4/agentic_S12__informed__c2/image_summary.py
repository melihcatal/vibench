from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_PROVIDER = "openai"


def image_summary(analysis: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Summarize the following image-analysis result in 2 concise sentences. "
        "Mention key labels, visible text, and safety findings if present.\n\n"
        f"Analysis JSON: {analysis}"
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize computer vision outputs for downstream asset catalogs."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    return {
        "provider": OPENAI_PROVIDER,
        "model": OPENAI_MODEL,
        "summary": text.strip(),
        "usage": response.usage.model_dump() if response.usage else None,
    }
