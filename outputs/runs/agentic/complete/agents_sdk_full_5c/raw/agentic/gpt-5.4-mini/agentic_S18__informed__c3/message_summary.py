from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from messaging_models import MessageSummary

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_message_results(results: Iterable[dict]) -> MessageSummary:
    client = OpenAI()
    text = "\n".join(str(item) for item in results)
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize message processing results succinctly."},
            {"role": "user", "content": text},
        ],
    )
    summary_text = completion.choices[0].message.content or ""
    total = len(list(results)) if hasattr(results, "__len__") else 0
    return MessageSummary(total=total, processed=total, failed=0, notes=[summary_text])
