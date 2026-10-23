from __future__ import annotations

from typing import Dict

from anthropic import Anthropic

ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def vendor_text_safety(text: str) -> Dict[str, str]:
    client = Anthropic()
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=128,
        messages=[{"role": "user", "content": f"Assess if this vendor note is safe. Return SAFE or UNSAFE with a brief reason: {text}"}],
    )
    content = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
    label = "SAFE" if "SAFE" in content.upper() and "UNSAFE" not in content.upper() else "UNSAFE"
    return {"label": label, "reason": content}
