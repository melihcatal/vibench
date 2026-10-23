from __future__ import annotations

from openai import AsyncOpenAI

from speech_models import normalize_whitespace


async def translate_live_caption(
    caption_text: str,
    *,
    target_language: str = "Spanish",
    source_language: str = "English",
    model: str = "gpt-4o-mini",
) -> str:
    client = AsyncOpenAI()
    prompt = (
        f"Translate the live caption from {source_language} to {target_language}. "
        "Keep timing-neutral wording and return only the translated caption.\n\n"
        f"Caption: {normalize_whitespace(caption_text)}"
    )
    response = await client.responses.create(
        model=model,
        input=prompt,
    )
    return normalize_whitespace(response.output_text)
