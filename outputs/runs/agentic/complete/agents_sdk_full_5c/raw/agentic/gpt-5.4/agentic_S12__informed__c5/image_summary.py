from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def summarize_visual_analysis(analysis_result: Dict[str, Any]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI")

    client = OpenAI(api_key=api_key)
    prompt = (
        "Summarize the following image analysis output into a concise paragraph with key labels, text, and safety findings.\n"
        + json.dumps(analysis_result, ensure_ascii=False)
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize visual understanding results."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    return {"provider": "openai", "model": MODEL_ID, "summary": text.strip()}
