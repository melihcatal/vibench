import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _message_content(message: Dict[str, Any]) -> str:
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return str(content)


def summarize_moderation_decisions(
    decisions: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt_lines = ["Summarize these moderation decisions clearly and concisely:"]
    for i, decision in enumerate(decisions, 1):
        status = decision.get("decision", decision.get("status", "unknown"))
        reason = decision.get("reason", decision.get("rationale", ""))
        text = decision.get("text", decision.get("message", ""))
        prompt_lines.append(f"{i}. decision: {status}; reason: {reason}; text: {text}")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a moderation operations assistant."},
            {"role": "user", "content": "\n".join(prompt_lines)},
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    return _message_content(message)
