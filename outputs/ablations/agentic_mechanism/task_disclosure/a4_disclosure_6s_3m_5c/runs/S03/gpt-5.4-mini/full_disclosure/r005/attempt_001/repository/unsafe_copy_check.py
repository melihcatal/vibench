import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("text", "content", "copy", "localized_copy"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        if "segments" in payload and isinstance(payload["segments"], list):
            return "\n".join(str(item) for item in payload["segments"])
        return json.dumps(payload, ensure_ascii=False)
    if isinstance(payload, list):
        return "\n".join(str(item) for item in payload)
    return str(payload)


def _post_openai(messages: List[Dict[str, str]], temperature: float = 0.0) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": temperature,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def check_unsafe_copy(localized_copy: Any, source_language: Optional[str] = None, target_language: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_text(localized_copy)
    context = []
    if source_language:
        context.append(f"source_language={source_language}")
    if target_language:
        context.append(f"target_language={target_language}")
    context_text = ", ".join(context) if context else "unknown languages"
    system_prompt = (
        "You are a safety reviewer for localized marketing and product copy. "
        "Identify unsafe content including hate, harassment, sexual content, self-harm, violence, illegal activity, "
        "deceptive claims, privacy leaks, and regulated content risks. Return strict JSON with keys: "
        "unsafe (boolean), severity (string), issues (array of strings), rationale (string), and suggested_fixes (array of strings)."
    )
    user_prompt = f"Review this localized copy for unsafe content. Context: {context_text}. Copy: {text}"
    result = _post_openai([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    content = result["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "unsafe": True,
            "severity": "unknown",
            "issues": ["model returned non-JSON output"],
            "rationale": content,
            "suggested_fixes": [],
        }
    return parsed
