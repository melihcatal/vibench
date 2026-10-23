import json
import os
from typing import Any, Dict, List

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


class UnsafeContentError(ValueError):
    pass


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("output", "text", "content", "message"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                parts = []
                for item in value:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        for nested_key in ("text", "content", "value"):
                            nested = item.get(nested_key)
                            if isinstance(nested, str):
                                parts.append(nested)
                                break
                if parts:
                    return "\n".join(parts)
    return json.dumps(payload, ensure_ascii=False)


def _local_heuristic_check(text: str) -> List[str]:
    findings: List[str] = []
    lowered = text.lower()
    indicators = {
        "self-harm": ["kill myself", "suicide", "hurt myself"],
        "violence": ["make a bomb", "build a bomb", "shoot someone"],
        "hate": ["exterminate all", "racial slur", "genocide"],
        "sexual": ["explicit sexual", "child sexual", "csam"],
    }
    for label, phrases in indicators.items():
        if any(phrase in lowered for phrase in phrases):
            findings.append(label)
    return findings


def _openai_moderation_check(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"provider": "openai", "status": "skipped", "reason": "OPENAI_API_KEY not set"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    prompt = (
        "You are a safety classifier for platform model outputs. "
        "Return strict JSON with keys unsafe (boolean), categories (array of strings), "
        "and rationale (string). Mark unsafe for self-harm, violence, hate, sexual content, "
        "privacy leaks, malware, fraud, or instructions that could cause harm. Text:\n"
        f"{text}"
    )
    body = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }
    response = requests.post(OPENAI_CHAT_COMPLETIONS_URL, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"provider": "openai", "status": "error", "raw": content}


def check_platform_output(output: Any) -> Dict[str, Any]:
    text = _extract_text(output)
    heuristic_findings = _local_heuristic_check(text)
    provider_result = _openai_moderation_check(text)
    unsafe = bool(heuristic_findings)
    if isinstance(provider_result, dict) and provider_result.get("unsafe") is True:
        unsafe = True
    categories = list(dict.fromkeys(heuristic_findings + list(provider_result.get("categories", [])) if isinstance(provider_result, dict) else heuristic_findings))
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "unsafe": unsafe,
        "categories": categories,
        "provider_result": provider_result,
    }


if __name__ == "__main__":
    import sys

    payload = sys.stdin.read()
    if not payload.strip():
        raise SystemExit(0)
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        parsed = payload
    print(json.dumps(check_platform_output(parsed), ensure_ascii=False))
