from __future__ import annotations

from anthropic import Anthropic

DEFAULT_SAFETY_MODEL = "claude-3-5-sonnet-latest"


def check_script_safety(text: str) -> dict:
    client = Anthropic()
    response = client.messages.create(model=DEFAULT_SAFETY_MODEL, max_tokens=256, messages=[{"role": "user", "content": f"Review this narration script for unsafe or disallowed content and return JSON with fields safe and reasons: {text}"}])
    content = response.content[0].text if response.content else ""
    return {"provider": "anthropic", "model": DEFAULT_SAFETY_MODEL, "analysis": content}
