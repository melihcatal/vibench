import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_text(text: str, source_language: str, target_language: str, api_key: Optional[str] = None) -> str:
    if not text:
        return text
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    prompt = (
        f"Translate the following text from {source_language} to {target_language}. "
        f"Return only the translated text, preserving meaning and style:\n{text}"
    )
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": prompt,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return _extract_output_text(data)


def _extract_output_text(data: Dict[str, Any]) -> str:
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            return data["output_text"].strip()
        output = data.get("output")
        if isinstance(output, list):
            parts = []
            for item in output:
                if not isinstance(item, dict):
                    continue
                content = item.get("content")
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict):
                            text = part.get("text")
                            if isinstance(text, str):
                                parts.append(text)
            if parts:
                return "".join(parts).strip()
    raise ValueError("Unexpected response format from OpenAI API")
