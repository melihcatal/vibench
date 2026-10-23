from __future__ import annotations

import os

from anthropic import Anthropic


def unsafe_copy_check(localized_copy: str) -> bool:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=32,
        messages=[
            {
                "role": "user",
                "content": f"Assess whether this localized copy contains unsafe content. Reply only with SAFE or UNSAFE.\n\n{localized_copy}",
            }
        ],
    )
    text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
    return text.strip().upper().startswith("SAFE")
