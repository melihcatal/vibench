import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def _extract_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        for key in ("text", "transcript", "content", "summary"):
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                return value
        for key in ("segments", "items", "results", "data"):
            value = obj.get(key)
            if isinstance(value, list):
                text = " ".join(_extract_text(item) for item in value)
                if text.strip():
                    return text
        return ""
    if isinstance(obj, list):
        return " ".join(_extract_text(item) for item in obj)
    return str(obj)


def _load_transcript(payload: Any) -> str:
    text = _extract_text(payload)
    if text.strip():
        return text
    raise ValueError("No transcript text found in payload")


def summarize_transcription_results(transcription_result: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    transcript_text = _load_transcript(transcription_result)
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Summarize transcription results for archival use."},
                {"role": "user", "content": transcript_text},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = ""
    if isinstance(data, dict):
        choices = data.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            summary = message.get("content") or ""
    if not summary.strip():
        summary = _extract_text(data)
    return {"summary": summary.strip(), "model": OPENAI_MODEL, "provider": "openai"}


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: archive_summary.py '<json_transcript>'")
    payload = json.loads(sys.argv[1])
    print(json.dumps(summarize_transcription_results(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()
