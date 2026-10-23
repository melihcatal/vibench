from __future__ import annotations

import os

from openai import OpenAI

from messaging_models import ProcessingRecord


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_message_processing(records: list[ProcessingRecord]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines = [
        f"message_id={r.message_id}; status={r.status}; safety={r.safety_label}; translated={bool(r.translated_text)}"
        for r in records
    ]
    prompt = "Summarize the following message processing results in a concise operational note:\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text.strip()
