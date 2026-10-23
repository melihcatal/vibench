import os
from typing import Any, Dict, List, Optional, Sequence

import requests


OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_CHAT_MODEL = "gpt-4.1-mini"


def _resolve_api_key(api_key: Optional[str]) -> str:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    return token


def _coerce_decision_text(decision: Dict[str, Any]) -> str:
    if "summary" in decision and decision["summary"] is not None:
        return str(decision["summary"])
    if "decision" in decision and decision["decision"] is not None:
        return str(decision["decision"])
    if decision.get("flagged") is True:
        return "flagged"
    if decision.get("flagged") is False:
        return "allowed"
    return "unknown"


def _render_input(decisions: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for index, decision in enumerate(decisions, start=1):
        message = str(decision.get("message", ""))
        label = _coerce_decision_text(decision)
        categories = decision.get("categories") or {}
        scores = decision.get("category_scores") or {}
        triggered = decision.get("triggered_categories") or {}
        lines.append(f"Item {index}:")
        lines.append(f"Message: {message}")
        lines.append(f"Decision: {label}")
        if categories:
            lines.append(f"Categories: {categories}")
        if scores:
            lines.append(f"Category scores: {scores}")
        if triggered:
            lines.append(f"Triggered thresholds: {triggered}")
        reason = decision.get("reason") or decision.get("rationale")
        if reason:
            lines.append(f"Reason: {reason}")
        lines.append("")
    return "\n".join(lines).strip()


def summarize_moderation_decisions(
    decisions: Sequence[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> Dict[str, Any]:
    token = _resolve_api_key(api_key)
    prompt = _render_input(decisions)
    response = requests.post(
        OPENAI_CHAT_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "Summarize moderation decisions concisely for a policy reviewer."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    choices = payload.get("choices") or []
    summary = ""
    if choices:
        message = choices[0].get("message") or {}
        summary = str(message.get("content") or "")
    return {"model": model, "summary": summary, "raw": payload}


def summarize_moderation_decisions_from_env(decisions: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    return summarize_moderation_decisions(decisions)
