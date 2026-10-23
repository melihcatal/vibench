"""Summarize retrieved document records using OpenAI chat completions."""
from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


def record_summary(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    prompt = {
        "role": "user",
        "content": f"Summarize these document records concisely as JSON with keys summary and highlights: {records}",
    }
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[prompt], temperature=0.2)
    text = response.choices[0].message.content or ""
    return {"model": "gpt-4o-mini", "summary_text": text}
