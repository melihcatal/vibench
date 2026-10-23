from __future__ import annotations

import os

from openai import OpenAI

from translation_models import TranslationQualityIssue

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_quality_issues(text: str) -> list[TranslationQualityIssue]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize translation quality issues in concise bullet points.",
            },
            {"role": "user", "content": text},
        ],
    )
    output = response.output_text.strip()
    return [TranslationQualityIssue(category="summary", message=line.strip("- ")) for line in output.splitlines() if line.strip()]
