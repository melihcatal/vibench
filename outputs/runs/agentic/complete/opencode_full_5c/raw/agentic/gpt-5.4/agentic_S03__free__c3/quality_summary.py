import json
from typing import Any, Dict, List

from translation_client import create_openai_response


def quality_summary(
    source_text: str, translated_text: str, source_language: str, target_language: str
) -> Dict[str, Any]:
    prompt = (
        "You are evaluating translation quality. "
        "Return strict JSON with keys summary, issues, severity. "
        f"Source language: {source_language}. Target language: {target_language}. "
        f"Source: {source_text}\nTranslated: {translated_text}"
    )
    payload = create_openai_response(prompt, model="gpt-4.1-mini")
    output_text = payload.get("output", [])[0].get("content", [])[0].get("text", "{}")
    parsed = json.loads(output_text)
    return {
        "provider": "openai_responses",
        "model": "gpt-4.1-mini",
        "summary": parsed.get("summary", ""),
        "issues": parsed.get("issues", [])
        if isinstance(parsed.get("issues", []), list)
        else [],
        "severity": parsed.get("severity", "unknown"),
    }
