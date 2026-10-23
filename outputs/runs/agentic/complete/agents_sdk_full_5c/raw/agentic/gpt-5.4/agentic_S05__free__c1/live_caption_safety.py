from __future__ import annotations

from anthropic import AsyncAnthropic

from speech_models import normalize_whitespace


async def check_live_caption_safety(
    caption_text: str,
    *,
    model: str = "claude-3-5-haiku-20241022",
) -> str:
    client = AsyncAnthropic()
    message = await client.messages.create(
        model=model,
        max_tokens=120,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    "Classify whether this live transcript text is unsafe. "
                    "Return one short label and a brief reason.\n\n"
                    f"Transcript: {normalize_whitespace(caption_text)}"
                ),
            }
        ],
    )
    parts = [block.text for block in message.content if getattr(block, "type", None) == "text"]
    return normalize_whitespace(" ".join(parts))
