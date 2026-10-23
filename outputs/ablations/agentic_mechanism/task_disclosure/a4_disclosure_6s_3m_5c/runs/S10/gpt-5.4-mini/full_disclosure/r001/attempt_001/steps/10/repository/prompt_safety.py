import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _client() -> requests.Session:
    session = requests.Session()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    session.headers.update({"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    return session


def _messages(prompt: str, text: str) -> str:
    return (
        "You are a strict safety classifier for prompts and generated text. "
        "Return only valid JSON with keys unsafe (boolean), categories (array of strings), and rationale (string). "
        "Classify content as unsafe if it contains self-harm, violence, hate, sexual content involving minors, wrongdoing instructions, or other clearly harmful material. "
        f"Prompt:\n{prompt}\n\nText:\n{text}"
    )


def check_prompt_safety(prompt: str, generated_text: Optional[str] = None) -> Dict[str, Any]:
    session = _client()
    payload = {
        "model": OPENAI_MODEL,
        "input": _messages(prompt, generated_text or ""),
        "temperature": 0,
    }
    response = session.post(OPENAI_API_URL, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    text = ""
    if isinstance(data, dict):
        if "output_text" in data and isinstance(data["output_text"], str):
            text = data["output_text"]
        else:
            output = data.get("output", [])
            for item in output:
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"}:
                        text += content.get("text", "")
    if not text:
        return {"unsafe": True, "categories": ["unknown"], "rationale": "No classifier output"}
    try:
        import json

        parsed = json.loads(text)
        if not isinstance(parsed, dict):
            raise ValueError
        parsed.setdefault("unsafe", True)
        parsed.setdefault("categories", ["unknown"])
        parsed.setdefault("rationale", "")
        return parsed
    except Exception:
        lowered = text.lower()
        return {
            "unsafe": any(token in lowered for token in ["unsafe", "harm", "violent", "sexual", "self-harm", "hate"]),
            "categories": ["unknown"],
            "rationale": text,
        }
