from __future__ import annotations

import json
import os
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_API_URL = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/") + "/responses"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    if isinstance(response_json.get("output_text"), str):
        return response_json["output_text"]
    parts = []
    for item in response_json.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
    return "".join(parts)


def translate_dictionary_values(
    values: Mapping[str, str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    if not isinstance(values, Mapping):
        raise TypeError("values must be a mapping")
    if not target_language:
        raise ValueError("target_language is required")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    keys = list(values.keys())
    payload = {str(key): "" if values[key] is None else str(values[key]) for key in keys}

    instructions = (
        "Translate the JSON object values into the target language while preserving all keys exactly. "
        "Return only a JSON object with the same keys in any order."
    )
    if source_language:
        instructions += f" Source language: {source_language}."

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TRANSLATION_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are a professional translation engine."}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{instructions}\nTarget language: {target_language}\nInput JSON:\n{json.dumps(payload, ensure_ascii=False)}",
                        }
                    ],
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    output_text = _extract_output_text(data).strip()
    if not output_text:
        raise RuntimeError("Empty translation response")

    translated = json.loads(output_text)
    if not isinstance(translated, dict):
        raise RuntimeError("Translation response must be a JSON object")

    result: Dict[str, str] = {}
    for key in keys:
        if key not in translated:
            raise RuntimeError(f"Missing translated value for key: {key}")
        result[key] = str(translated[key])
    return result
