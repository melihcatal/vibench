from __future__ import annotations

import json
from typing import Any

from translation_client import OPENAI_DEFAULT_MODEL, openai_text_response


def quality_summary(
    source_text: str, translated_text: str, source_language: str, target_language: str
) -> dict[str, Any]:
    system_prompt = (
        "You are a translation QA reviewer. Return strict JSON with keys: summary, issues, severity. "
        "issues must be a list of short strings and severity must be one of low, medium, high."
    )
    user_input = json.dumps(
        {
            "model": OPENAI_DEFAULT_MODEL,
            "source_text": source_text,
            "translated_text": translated_text,
            "source_language": source_language,
            "target_language": target_language,
        },
        ensure_ascii=False,
    )
    content = openai_text_response(system_prompt, user_input)
    data = json.loads(content)
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_MODEL,
        "summary": data["summary"],
        "issues": data["issues"],
        "severity": data["severity"],
    }
