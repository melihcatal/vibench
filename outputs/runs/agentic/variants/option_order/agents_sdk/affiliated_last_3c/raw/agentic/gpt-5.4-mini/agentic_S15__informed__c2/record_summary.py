from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI

PROVIDER_NAME = "OpenAI"
MODEL_ID = "gpt-4o-mini"


def summarize_records(records: List[Dict[str, Any]], prompt_prefix: str = "Summarize these document records concisely.") -> str:
    client = OpenAI()
    prompt = f"{prompt_prefix}\n\n{records}"
    response = client.chat.completions.create(model=MODEL_ID, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""
