from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def _normalize_decision(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "message_id": decision.get("message_id"),
        "decision": decision.get("decision"),
        "categories": decision.get("categories", {}),
        "rationale": decision.get("rationale", ""),
    }


def _build_prompt(decisions: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    normalized = [_normalize_decision(d) for d in decisions]
    user_content = json.dumps(normalized, ensure_ascii=False, indent=2)
    return [
        {
            "role": "system",
            "content": (
                "You are a moderation operations assistant. Summarize a batch of moderation decisions "
                "into a concise review brief. Focus on overall patterns, key risks, and notable exceptions. "
                "Do not invent facts."
            ),
        },
        {
            "role": "user",
            "content": (
                "Summarize these moderation decisions for a human reviewer. "
                "Return a short paragraph and then 3-5 bullet points.\n\n"
                f"{user_content}"
            ),
        },
    ]


def summarize_moderation_decisions(decisions: Iterable[Dict[str, Any]], timeout: int = 30) -> str:
    payload = {
        "model": OPENAI_MODEL,
        "messages": _build_prompt(decisions),
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {_get_api_key()}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def summarize_from_json(text: str, timeout: int = 30) -> str:
    decisions = json.loads(text)
    if not isinstance(decisions, list):
        raise ValueError("Expected a JSON list of moderation decisions")
    return summarize_moderation_decisions(decisions, timeout=timeout)
