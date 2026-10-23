from __future__ import annotations

from anthropic import Anthropic
import os


def welcome_translate(text: str, target_locale: str) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Translate the following onboarding copy into {target_locale}. Keep meaning, tone, and formatting. Return only the translated text.\n\n{text}"}
        ],
    )
    return "".join(block.text for block in message.content if hasattr(block, "text"))
