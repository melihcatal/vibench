from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI

from vision_models import SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def summarize_visual_analysis(analysis: Dict[str, Any]) -> SummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Summarize the following image-analysis outputs in 3 concise sentences, "
        "covering scene, text, and safety implications when present:\n"
        f"{json.dumps(analysis, ensure_ascii=False)}"
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize visual analysis results for downstream product metadata."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    return SummaryResult(summary=text.strip(), model=OPENAI_MODEL)
