import os
from typing import Optional

import anthropic


def summarize_translation_quality(
    original_text: str,
    translated_text: str,
    source_lang: str = "auto",
    target_lang: str = "en",
    focus_areas: Optional[list[str]] = None,
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    areas = (
        ", ".join(focus_areas)
        if focus_areas
        else "accuracy, fluency, tone, terminology, cultural appropriateness"
    )

    system_prompt = (
        "You are a professional translation quality analyst. Analyze the provided translation "
        f"and produce a concise quality summary. Focus on: {areas}. "
        "Return a structured summary with: overall quality rating (1-5), key strengths, "
        "identified issues, and recommendations. Keep the response under 300 words."
    )

    user_prompt = (
        f"Source Language: {source_lang}\n"
        f"Target Language: {target_lang}\n\n"
        f"Original Text:\n{original_text}\n\n"
        f"Translated Text:\n{translated_text}"
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    return message.content[0].text
