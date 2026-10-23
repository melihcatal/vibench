from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class OpenAITranslateConfig:
    api_key: str = os.environ.get("OPENAI_API_KEY", "")
    model: str = os.environ.get("OPENAI_TRANSLATE_MODEL", "gpt-5.4-mini")
    api_base: str = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


class OpenAIRecordTranslator:
    def __init__(self, config: Optional[OpenAITranslateConfig] = None) -> None:
        self.config = config or OpenAITranslateConfig()
        if not self.config.api_key:
            raise ValueError("Missing OpenAI API key")
        self._session = requests.Session()

    def translate_record(
        self,
        record: Dict[str, Any],
        target_language: str,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        if not isinstance(record, dict):
            raise TypeError("record must be a dict")
        if not target_language:
            raise ValueError("target_language is required")

        prompt = self._build_prompt(record, target_language, fields)
        response = self._session.post(
            f"{self.config.api_base.rstrip('/')}/responses",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.config.model,
                "input": prompt,
                "temperature": 0.1,
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        text = self._extract_text(payload)
        if text:
            try:
                result = json.loads(text)
                if isinstance(result, dict):
                    result.setdefault("provider", "openai")
                    result.setdefault("model", self.config.model)
                    return result
            except json.JSONDecodeError:
                pass
        return {
            "translated_record": record,
            "provider": "openai",
            "model": self.config.model,
            "target_language": target_language,
        }

    @staticmethod
    def _build_prompt(record: Dict[str, Any], target_language: str, fields: Optional[List[str]]) -> str:
        if fields:
            field_list = ", ".join(fields)
            scope = f"Translate only these fields: {field_list}."
        else:
            scope = "Translate all user-facing text fields."
        return (
            "Translate the following document record into the target language. "
            f"Target language: {target_language}. {scope} "
            "Preserve all non-text data, keys, and structure. Return a JSON object with keys translated_record, translated_fields, and target_language. "
            f"Record: {json.dumps(record, ensure_ascii=False, separators=(\",\",\":\"))}"
        )

    @staticmethod
    def _extract_text(payload: Dict[str, Any]) -> str:
        output = payload.get("output", [])
        parts: List[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue
            for content in item.get("content", []):
                if isinstance(content, dict):
                    text = content.get("text")
                    if isinstance(text, str):
                        parts.append(text)
        return "\n".join(parts).strip()


def record_translate(record: Dict[str, Any], target_language: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
    return OpenAIRecordTranslator().translate_record(record, target_language, fields=fields)


def main() -> None:
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("Usage: record_translate.py '{\"title\":\"Hello\"}' 'es'")
    record = json.loads(sys.argv[1])
    target_language = sys.argv[2]
    result = record_translate(record, target_language)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
