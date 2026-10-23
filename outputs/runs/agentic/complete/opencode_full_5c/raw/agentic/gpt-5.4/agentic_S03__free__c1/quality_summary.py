from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def quality_summary(
    issues: Iterable[str], source_language: str, target_language: str
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    issue_list: List[str] = [str(issue) for issue in issues]
    prompt = (
        f"Summarize translation quality issues for {source_language} to {target_language}. "
        f"Focus on accuracy, fluency, terminology, and formatting. Issues: {issue_list}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
