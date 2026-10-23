import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class RunbookTranslationResult:
    provider: str
    source_language: str
    target_language: str
    source_text: str
    translated_text: str
    model: str


def _openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def _openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def translate_runbook_notes(notes: str, target_language: str, source_language: Optional[str] = None) -> RunbookTranslationResult:
    payload: Dict[str, Any] = {
        "model": _openai_model(),
        "input": [
            {
                "role": "system",
                "content": "You translate secret-rotation runbook notes accurately and preserve operational meaning.",
            },
            {
                "role": "user",
                "content": f"Translate the following runbook notes into {target_language}. Preserve bullet structure, commands, resource names, and safety warnings.\n\n{notes}",
            },
        ],
    }
    if source_language:
        payload["input"][1]["content"] = f"Translate the following runbook notes from {source_language} into {target_language}. Preserve bullet structure, commands, resource names, and safety warnings.\n\n{notes}"
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {_openai_api_key()}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translated_text = data.get("output_text") or ""
    if not translated_text:
        output = data.get("output", [])
        parts = []
        for item in output:
            for content in item.get("content", []):
                text = content.get("text")
                if text:
                    parts.append(text)
        translated_text = "".join(parts)
    return RunbookTranslationResult(
        provider="openai",
        source_language=source_language or "auto",
        target_language=target_language,
        source_text=notes,
        translated_text=translated_text,
        model=_openai_model(),
    )


def main() -> None:
    notes = os.getenv("RUNBOOK_NOTES")
    target_language = os.getenv("TARGET_LANGUAGE")
    if not notes or not target_language:
        raise RuntimeError("RUNBOOK_NOTES and TARGET_LANGUAGE environment variables are required")
    source_language = os.getenv("SOURCE_LANGUAGE")
    result = translate_runbook_notes(notes, target_language, source_language)
    print(json.dumps(result.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main()
