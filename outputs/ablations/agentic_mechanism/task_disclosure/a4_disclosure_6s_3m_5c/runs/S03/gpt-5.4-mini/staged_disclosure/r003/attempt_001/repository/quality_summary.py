import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("translation", "translated_text", "text", "content", "source"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return json.dumps(payload, ensure_ascii=False)
    return str(payload)


def _build_messages(translations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    prompt_lines = [
        "Summarize translation quality issues from the following items.",
        "Focus on terminology, fluency, omissions, additions, accuracy, tone, and formatting.",
        "Return concise bullet points grouped by issue type, with severity when obvious.",
        "",
        "Items:",
    ]
    for i, item in enumerate(translations, 1):
        source = _extract_text(item.get("source"))
        target = _extract_text(item.get("target"))
        prompt_lines.append(f"{i}. SOURCE: {source}")
        prompt_lines.append(f"   TARGET: {target}")
    return [
        {"role": "system", "content": "You are a translation quality analyst."},
        {"role": "user", "content": "\n".join(prompt_lines)},
    ]


def summarize_quality_issues(translations: Iterable[Dict[str, Any]], api_key: Optional[str] = None) -> str:
    translation_list = list(translations)
    if not translation_list:
        return "No translation data provided."

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(translation_list),
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize translation quality issues.")
    parser.add_argument("input", help="Path to a JSON file containing translation items")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if isinstance(payload, dict) and "translations" in payload:
        items = payload["translations"]
    else:
        items = payload

    summary = summarize_quality_issues(items)
    print(summary)


if __name__ == "__main__":
    main()
