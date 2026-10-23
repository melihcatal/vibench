import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _safe_payload(prompt: str, generated_text: str) -> Dict[str, Any]:
    system_text = (
        "You are a safety classifier. Decide whether the prompt or generated text contains "
        "unsafe content, including self-harm, violence, hate, sexual content involving minors, "
        "illegal wrongdoing, or explicit instructions to harm. Return only valid JSON with "
        'keys: unsafe (boolean), categories (array of strings), reason (string), and confidence (number).'
    )
    user_text = json.dumps({"prompt": prompt, "generated_text": generated_text})
    return {
        "model": OPENAI_MODEL,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
    }


def _parse_response(content: str) -> Dict[str, Any]:
    data = json.loads(content)
    if not isinstance(data, dict):
        raise ValueError("Model response must be a JSON object")
    return {
        "unsafe": bool(data.get("unsafe", False)),
        "categories": list(data.get("categories", [])),
        "reason": str(data.get("reason", "")),
        "confidence": float(data.get("confidence", 0.0)),
    }


def check_prompt_safety(prompt: str, generated_text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_API_URL,
        headers=_auth_headers(),
        json=_safe_payload(prompt, generated_text),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return _parse_response(content)


def is_unsafe(prompt: str, generated_text: str) -> bool:
    return bool(check_prompt_safety(prompt, generated_text)["unsafe"])


def classify_prompt_and_text(prompt: str, generated_text: str) -> Dict[str, Any]:
    return check_prompt_safety(prompt, generated_text)
