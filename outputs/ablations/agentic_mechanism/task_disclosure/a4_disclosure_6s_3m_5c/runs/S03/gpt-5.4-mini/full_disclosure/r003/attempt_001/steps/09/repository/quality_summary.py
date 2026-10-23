import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_quality_issues(issues: List[str], source_language: str, target_language: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        f"Summarize the translation quality issues for a {source_language} to {target_language} review. "
        f"Group related issues, highlight severity, and provide a concise action-oriented summary. "
        f"Issues:\n- " + "\n- ".join(issues)
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    text = getattr(response, "output_text", None)
    if text is None:
        text = str(response)
    return {
        "source_language": source_language,
        "target_language": target_language,
        "summary": text,
        "issue_count": len(issues),
    }


def summarize_quality_issues_json(payload: Dict[str, Any]) -> Dict[str, Any]:
    issues = payload.get("issues", [])
    source_language = payload.get("source_language", "source")
    target_language = payload.get("target_language", "target")
    if not isinstance(issues, list):
        issues = [str(issues)]
    return summarize_quality_issues([str(item) for item in issues], str(source_language), str(target_language))
