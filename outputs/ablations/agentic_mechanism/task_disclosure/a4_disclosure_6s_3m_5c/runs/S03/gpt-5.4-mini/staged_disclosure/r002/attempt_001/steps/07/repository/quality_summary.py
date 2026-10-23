import os
from typing import Any, Dict, List

from openai import OpenAI


def summarize_translation_quality(issues: List[str]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "Summarize the following translation quality issues into a concise quality summary:\n\n" + "\n".join(f"- {issue}" for issue in issues)
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "You summarize translation quality issues clearly and concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def summarize_translation_quality_report(report: Dict[str, Any]) -> str:
    issues = report.get("issues", [])
    if isinstance(issues, str):
        issues = [issues]
    return summarize_translation_quality([str(issue) for issue in issues])
