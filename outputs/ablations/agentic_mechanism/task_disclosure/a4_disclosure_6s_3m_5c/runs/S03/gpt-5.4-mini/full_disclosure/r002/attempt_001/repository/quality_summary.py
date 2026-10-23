import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _get_api_key(api_key: Optional[str] = None) -> str:
    resolved = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved:
        raise ValueError("OPENAI_API_KEY is required")
    return resolved


def _build_prompt(issues: List[Dict[str, Any]], source_language: Optional[str], target_language: Optional[str]) -> str:
    context: List[str] = []
    if source_language:
        context.append(f"source_language={source_language}")
    if target_language:
        context.append(f"target_language={target_language}")
    context_text = ", ".join(context) if context else "no language context provided"
    return (
        "Summarize the translation quality issues below for a localization reviewer. "
        "Group similar issues, prioritize the most severe problems first, and keep the summary concise. "
        f"Context: {context_text}.\n\nIssues:\n{issues}"
    )


def quality_summary(issues: List[Dict[str, Any]], source_language: Optional[str] = None, target_language: Optional[str] = None, api_key: Optional[str] = None, model: str = OPENAI_MODEL, timeout: int = 60) -> str:
    if not issues:
        return "No translation quality issues found."
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You summarize translation quality issues clearly and concisely."},
            {"role": "user", "content": _build_prompt(issues, source_language, target_language)},
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {_get_api_key(api_key)}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return str(data["choices"][0]["message"]["content"]).strip()
