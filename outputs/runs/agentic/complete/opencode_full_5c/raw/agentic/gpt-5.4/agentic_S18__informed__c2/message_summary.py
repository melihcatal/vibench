from __future__ import annotations

import json
import os
from typing import Any, Dict

from openai import OpenAI

from messaging_models import ProcessingSummary, utc_now_iso


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_message_result(
    source_message_id: str, processing_result: Dict[str, Any]
) -> ProcessingSummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarize message processing results in one concise sentence.",
            },
            {
                "role": "user",
                "content": json.dumps(processing_result, ensure_ascii=False),
            },
        ],
        temperature=0,
    )
    summary = response.choices[0].message.content or ""
    return ProcessingSummary(
        provider="openai",
        model=OPENAI_MODEL,
        source_message_id=source_message_id,
        summary=summary.strip(),
        created_at=utc_now_iso(),
    )
