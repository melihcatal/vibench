import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "openai/gpt-4.1-mini"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _build_input(prompt: str, generated_text: str) -> List[Dict[str, Any]]:
    system = (
        "You are a safety classifier for prompts and generated text. "
        "Assess whether the content includes unsafe instructions, self-harm, violence, hate, harassment, sexual content, "
        "privacy invasion, fraud, malware, or other policy-violating content. "
        "Return only valid JSON with keys safe (boolean), categories (array of strings), and rationale (string)."
    )
    user = {
        "prompt": prompt,
        "generated_text": generated_text,
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": str(user)},
    ]


def check_prompt_safety(prompt: str, generated_text: str, timeout: float = 30.0) -> Dict[str, Any]:
    payload = {
        "model": OPENAI_MODEL,
        "input": _build_input(prompt, generated_text),
        "response_format": {"type": "json_object"},
    }
    response = requests.post(OPENAI_API_URL, headers=_headers(), json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")
    if not text and isinstance(data.get("output_text"), str):
        text = data["output_text"]
    if not text:
        raise RuntimeError("No safety classification returned by OpenAI API")
    import json

    return json.loads(text)
