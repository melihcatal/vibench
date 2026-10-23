import os
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _resolve_api_key(api_key: Optional[str]) -> str:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    return token


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _extract_brief(decision: Dict[str, Any]) -> str:
    for key in ("brief", "summary", "rationale", "reason", "decision_text"):
        value = decision.get(key)
        if value:
            return _coerce_text(value)
    flagged = decision.get("flagged")
    if flagged is True:
        return "Flagged for reviewer attention."
    if flagged is False:
        return "No policy issue detected."
    return "Review required."


def _render_script(decisions: Sequence[Dict[str, Any]]) -> str:
    parts: List[str] = ["Moderation reviewer brief."]
    for index, decision in enumerate(decisions, start=1):
        message = _coerce_text(decision.get("message") or decision.get("text"))
        label = _coerce_text(decision.get("decision") or decision.get("status") or decision.get("label"))
        brief = _extract_brief(decision)
        segment = [f"Item {index}."]
        if message:
            segment.append(f"Message: {message}.")
        if label:
            segment.append(f"Decision: {label}.")
        segment.append(f"Brief: {brief}.")
        parts.append(" ".join(segment))
    return " ".join(parts).strip()


def generate_reviewer_brief_audio(
    decisions: Sequence[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
    voice: str = "alloy",
    response_format: str = "mp3",
) -> Dict[str, Any]:
    token = _resolve_api_key(api_key)
    input_text = _render_script(decisions)
    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": input_text,
            "voice": voice,
            "response_format": response_format,
        },
        timeout=60,
    )
    response.raise_for_status()
    return {"model": model, "voice": voice, "response_format": response_format, "audio": response.content, "text": input_text}


def generate_reviewer_brief_audio_from_env(decisions: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    return generate_reviewer_brief_audio(decisions)
