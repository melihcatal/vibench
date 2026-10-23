from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI

from messaging_models import ProcessingSummary


MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_message_processing(results: Iterable[Dict[str, Any]]) -> ProcessingSummary:
    items: List[Dict[str, Any]] = list(results)
    successful = sum(1 for item in items if item.get("status") == "success")
    failed = len(items) - successful
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "task": "Summarize message processing outcomes for operators in 2-4 concise sentences.",
        "results": items,
    }
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize queue processing outcomes for an operations dashboard."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        temperature=0.2,
    )
    notes = response.choices[0].message.content or ""
    return ProcessingSummary(
        total_messages=len(items),
        successful_messages=successful,
        failed_messages=failed,
        notes=notes,
    )
