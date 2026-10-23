from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class OpenAIConfig:
    api_key: str = os.environ.get("OPENAI_API_KEY", "")
    model: str = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")
    api_base: str = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")


class OpenAIRecordSummarizer:
    def __init__(self, config: Optional[OpenAIConfig] = None) -> None:
        self.config = config or OpenAIConfig()
        if not self.config.api_key:
            raise ValueError("Missing OpenAI API key")
        self._session = requests.Session()

    def summarize_records(self, records: List[Dict[str, Any]], style: str = "concise") -> Dict[str, Any]:
        if not isinstance(records, list):
            raise TypeError("records must be a list")
        if not records:
            return {"summary": "No records provided.", "model": self.config.model, "record_count": 0}
        prompt = (
            "Summarize these retrieved document records for a user. "
            f"Style: {style}. Return a JSON object with keys summary, highlights, and record_count. "
            f"Records: {json.dumps(records, ensure_ascii=False, separators=(\",\",\":\"))}"
        )
        response = self._session.post(
            f"{self.config.api_base.rstrip('/')}/responses",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.config.model,
                "input": prompt,
                "temperature": 0.2,
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
                    result.setdefault("model", self.config.model)
                    result.setdefault("record_count", len(records))
                    return result
            except json.JSONDecodeError:
                pass
        return {"summary": text or "Unable to generate summary.", "model": self.config.model, "record_count": len(records)}

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


def summarize_records(records: List[Dict[str, Any]], style: str = "concise") -> Dict[str, Any]:
    return OpenAIRecordSummarizer().summarize_records(records, style=style)


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: record_summary.py '[{""id"": ""1""}]'")
    records = json.loads(sys.argv[1])
    result = summarize_records(records)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
