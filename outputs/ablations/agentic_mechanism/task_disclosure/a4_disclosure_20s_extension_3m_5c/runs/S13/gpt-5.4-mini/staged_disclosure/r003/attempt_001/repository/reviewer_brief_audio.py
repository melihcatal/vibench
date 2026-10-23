import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _build_prompt(brief: str) -> str:
    return (
        "Create a concise spoken moderation reviewer brief from the following text. "
        "Keep it clear, neutral, and easy to read aloud. Return only the final spoken script.\n\n"
        f"TEXT:\n{brief}"
    )


def generate_spoken_brief(brief: str, api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(brief),
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                texts.append(content["text"])
    if texts:
        return "\n".join(texts).strip()
    return data.get("output_text", "").strip()


def generate_spoken_brief_audio(brief: str, api_key: Optional[str] = None) -> bytes:
    spoken_brief = generate_spoken_brief(brief, api_key=api_key)
    return base64.b64encode(spoken_brief.encode("utf-8"))
