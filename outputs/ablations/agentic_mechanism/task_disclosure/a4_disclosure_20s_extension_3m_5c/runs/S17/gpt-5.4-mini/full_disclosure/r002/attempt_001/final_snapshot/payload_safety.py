import base64
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, bytes):
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError:
            return base64.b64encode(payload).decode("ascii")
    if isinstance(payload, dict):
        for key in ("text", "plaintext", "payload", "content"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        return str(payload)
    return str(payload)


def _build_prompt(text: str) -> str:
    return (
        "Analyze the following decrypted text payload for unsafe content, including "
        "malware instructions, credential theft, secrets exposure, phishing, violence, "
        "self-harm, illicit activity, or sensitive data leakage. Return JSON with keys "
        '"safe" (boolean), "risk_level" (one of low, medium, high), and "findings" '
        f"(array of short strings). Payload: {text}"
    )


def _default_result() -> Dict[str, Any]:
    return {"safe": True, "risk_level": "low", "findings": []}


def check_payload_safety(payload: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_text(payload)
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"safe": False, "risk_level": "high", "findings": ["missing OPENAI_API_KEY"]}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(text),
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    body = response.json()

    output_text = ""
    if isinstance(body, dict):
        if "output_text" in body and isinstance(body["output_text"], str):
            output_text = body["output_text"]
        else:
            outputs = body.get("output", [])
            for item in outputs:
                content = item.get("content", []) if isinstance(item, dict) else []
                for part in content:
                    if isinstance(part, dict) and part.get("type") in {"output_text", "text"}:
                        output_text += part.get("text", "")

    if not output_text:
        return _default_result()

    try:
        import json

        parsed = json.loads(output_text)
        if isinstance(parsed, dict):
            return {
                "safe": bool(parsed.get("safe", True)),
                "risk_level": str(parsed.get("risk_level", "low")),
                "findings": list(parsed.get("findings", [])) if isinstance(parsed.get("findings", []), list) else [],
            }
    except Exception:
        pass

    lowered = output_text.lower()
    return {
        "safe": "unsafe" not in lowered and "high risk" not in lowered,
        "risk_level": "medium" if "medium" in lowered else ("high" if ("unsafe" in lowered or "high" in lowered) else "low"),
        "findings": [output_text[:500]],
    }
