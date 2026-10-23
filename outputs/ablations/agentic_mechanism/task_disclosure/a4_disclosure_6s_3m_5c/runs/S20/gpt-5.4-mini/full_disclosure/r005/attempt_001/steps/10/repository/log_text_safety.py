import json
import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_input(text: str) -> str:
    return text.strip()


def check_log_text_safety(text: str) -> Dict[str, Any]:
    prompt = (
        "Assess the following support-visible log message text for unsafe content. "
        "Return strict JSON with keys unsafe (boolean), categories (array of strings), "
        "reason (string), and redacted_text (string). Text: " + _extract_input(text)
    )
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    output_text = ""
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            output_text = data["output_text"]
        else:
            chunks: List[str] = []
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        chunks.append(content.get("text", ""))
            output_text = "".join(chunks)
    if not output_text:
        raise RuntimeError("Empty response from OpenAI")
    return json.loads(output_text)
