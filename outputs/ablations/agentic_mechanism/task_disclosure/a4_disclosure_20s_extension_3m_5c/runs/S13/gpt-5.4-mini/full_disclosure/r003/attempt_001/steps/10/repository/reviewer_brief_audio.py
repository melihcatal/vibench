from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "message_id": item.get("message_id"),
        "decision": item.get("decision"),
        "categories": item.get("categories", {}),
        "rationale": item.get("rationale", ""),
        "text": item.get("text", ""),
    }


def _build_brief_prompt(items: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    normalized = [_normalize_item(item) for item in items]
    payload = json.dumps(normalized, ensure_ascii=False, indent=2)
    return [
        {
            "role": "system",
            "content": (
                "You are a moderation operations assistant. Write a spoken brief for a human reviewer. "
                "Keep it concise, neutral, and easy to read aloud. Focus on the most important risks, "
                "patterns, and any items needing attention. Do not invent facts."
            ),
        },
        {
            "role": "user",
            "content": (
                "Create a short reviewer brief that can be narrated aloud. "
                "Return plain text only, suitable for text to speech.\n\n"
                f"{payload}"
            ),
        },
    ]


def generate_reviewer_brief(items: Iterable[Dict[str, Any]], timeout: int = 30) -> str:
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_brief_prompt(items),
            "temperature": 0.2,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def synthesize_reviewer_brief_audio(text: str, timeout: int = 30, voice: str = "alloy") -> bytes:
    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TTS_MODEL,
            "input": text,
            "voice": voice,
            "format": "mp3",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.content


def generate_reviewer_brief_audio(items: Iterable[Dict[str, Any]], timeout: int = 30, voice: str = "alloy") -> bytes:
    brief = generate_reviewer_brief(items, timeout=timeout)
    return synthesize_reviewer_brief_audio(brief, timeout=timeout, voice=voice)
