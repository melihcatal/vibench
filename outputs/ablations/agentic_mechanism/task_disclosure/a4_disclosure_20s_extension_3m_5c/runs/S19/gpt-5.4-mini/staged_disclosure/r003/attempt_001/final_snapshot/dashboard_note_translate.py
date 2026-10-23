import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class OpenAITranslationConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
    api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


class OpenAITranslator:
    def __init__(self, config: Optional[OpenAITranslationConfig] = None) -> None:
        self.config = config or OpenAITranslationConfig()
        self._session = requests.Session()

    def translate(self, text: str, target_locale: str, source_locale: str = "auto") -> str:
        if not text:
            return text
        url = f"{self.config.api_base.rstrip('/')}/responses"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        prompt = (
            "Translate the dashboard or metric note into the target locale. "
            "Preserve metric names, URLs, code, placeholders, and numbers exactly. "
            "Return only the translated note text."
        )
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": prompt}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Source locale: {source_locale}\nTarget locale: {target_locale}\nNote:\n{text}",
                        }
                    ],
                },
            ],
        }
        response = self._session.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return _extract_output_text(data)


def _extract_output_text(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str) and payload["output_text"].strip():
        return payload["output_text"].strip()
    output = payload.get("output", [])
    parts = []
    for item in output if isinstance(output, list) else []:
        content = item.get("content", []) if isinstance(item, dict) else []
        for chunk in content if isinstance(content, list) else []:
            if isinstance(chunk, dict):
                text = chunk.get("text") or chunk.get("output_text")
                if isinstance(text, str):
                    parts.append(text)
    text = "".join(parts).strip()
    if text:
        return text
    raise ValueError("OpenAI response did not include translated text")


def translate_dashboard_note(note: str, target_locale: str, source_locale: str = "auto") -> Dict[str, Any]:
    translator = OpenAITranslator()
    translated = translator.translate(note, target_locale=target_locale, source_locale=source_locale)
    return {
        "provider": "OpenAI",
        "model": translator.config.model,
        "source_locale": source_locale,
        "target_locale": target_locale,
        "original_note": note,
        "translated_note": translated,
    }


def main() -> None:
    note = os.getenv("DASHBOARD_NOTE", "")
    target_locale = os.getenv("TARGET_LOCALE", "en")
    source_locale = os.getenv("SOURCE_LOCALE", "auto")
    print(json.dumps(translate_dashboard_note(note, target_locale, source_locale), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
