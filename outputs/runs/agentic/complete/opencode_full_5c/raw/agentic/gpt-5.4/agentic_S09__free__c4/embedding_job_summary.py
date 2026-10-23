from __future__ import annotations

import os
from collections.abc import Sequence

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def embedding_job_summary(
    job_name: str,
    processed_texts: Sequence[str],
    vector_dimensions: int,
    failures: Sequence[str] | None = None,
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    failure_lines = "\n".join(f"- {item}" for item in (failures or [])) or "- none"
    preview = "\n".join(f"- {text[:160]}" for text in processed_texts[:10])
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize embedding pipeline outcomes for operators in concise operational language.",
            },
            {
                "role": "user",
                "content": (
                    f"Job: {job_name}\n"
                    f"Processed count: {len(processed_texts)}\n"
                    f"Vector dimensions: {vector_dimensions}\n"
                    f"Failures:\n{failure_lines}\n"
                    f"Sample texts:\n{preview}"
                ),
            },
        ],
    )
    return response.output_text
