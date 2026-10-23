from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_QUALITY_MODEL = "gpt-4.1-mini"


def summarize_translation_quality(
    source_text: str, translated_text: str, issues: Iterable[str]
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issue_list: List[str] = [str(item) for item in issues]
    prompt = {
        "source_text": source_text,
        "translated_text": translated_text,
        "issues": issue_list,
        "task": "Summarize translation quality problems concisely with severity and likely remediation.",
    }
    response = client.responses.create(
        model=OPENAI_QUALITY_MODEL,
        input=[
            {
                "role": "system",
                "content": "You evaluate localization quality and return concise plain text summaries.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.output_text
