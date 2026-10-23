from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from translation_models import QualityIssue


def summarize_quality_issues(issues: Iterable[QualityIssue]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "Summarize these translation quality issues concisely:\n" + "\n".join(
        f"- {issue.category} [{issue.severity}]: {issue.message}" for issue in issues
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize translation QA findings."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
