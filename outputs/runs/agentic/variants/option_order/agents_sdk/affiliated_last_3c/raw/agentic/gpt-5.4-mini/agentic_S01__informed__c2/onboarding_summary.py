from __future__ import annotations

from typing import Any, Dict

import anthropic

MODEL_ID = "claude-3-5-sonnet-20240620"


def onboarding_summary(onboarding_state: Dict[str, Any]) -> Dict[str, str]:
    client = anthropic.Anthropic(api_key=__import__("os").environ.get("ANTHROPIC_API_KEY", ""))
    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support in one concise paragraph: {onboarding_state}",
            }
        ],
    )
    text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
    return {"summary": text, "model": MODEL_ID, "provider": "Anthropic Messages API"}
