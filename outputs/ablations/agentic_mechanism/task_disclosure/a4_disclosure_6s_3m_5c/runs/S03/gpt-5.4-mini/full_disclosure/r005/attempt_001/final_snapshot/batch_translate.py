from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def _normalize_inputs(texts: List[str], source_language: Optional[str], target_language: str) -> Dict[str, Any]:
    return {
        "texts": texts,
        "source_language": source_language,
        "target_language": target_language,
    }


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    if "output_text" in response_json and isinstance(response_json["output_text"], str):
        return response_json["output_text"]
    output = response_json.get("output", [])
    parts: List[str] = []
    for item in output:
        content = item.get("content", []) if isinstance(item, dict) else []
        for part in content:
            if isinstance(part, dict) and part.get("type") in {"output_text", "text"}:
                text = part.get("text")
                if isinstance(text, str):
                    parts.append(text)
    return "".join(parts)


def batch_translate(texts: List[str], target_language: str, source_language: Optional[str] = None) -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = _normalize_inputs(texts, source_language, target_language)
    instructions = (
        "Translate each string independently and preserve the original list order. "
        "Return only a JSON array of translated strings with the same length as the input."
    )
    if source_language:
        instructions += f" Source language: {source_language}."

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": f"Translate these strings to {target_language}: {payload['texts']}",
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output_text = _extract_output_text(data).strip()
    if not output_text:
        raise RuntimeError("Empty translation response")

    try:
        import json

        translated = json.loads(output_text)
    except Exception as exc:
        raise RuntimeError(f"Failed to parse translation response: {output_text}") from exc

    if not isinstance(translated, list):
        raise RuntimeError("Translation response must be a JSON array")
    if len(translated) != len(texts):
        raise RuntimeError("Translation response length mismatch")
    return [str(item) for item in translated]
