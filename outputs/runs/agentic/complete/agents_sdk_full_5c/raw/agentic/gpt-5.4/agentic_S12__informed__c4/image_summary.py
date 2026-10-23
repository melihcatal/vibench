from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI


MODEL = "gpt-4o-mini"


def summarize_visual_analysis(analysis: Dict[str, Any]) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize image analysis results into a concise operational summary with key labels, OCR text, "
        "and safety concerns. Return plain text only.\n\n"
        f"Analysis JSON:\n{json.dumps(analysis, ensure_ascii=False)}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize computer vision outputs for downstream workflows."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    return {"provider": "OpenAI", "model": MODEL, "summary": text.strip()}
