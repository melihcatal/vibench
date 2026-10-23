from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import DEFAULT_TRANSLATION_MODEL, get_client


def localized_platform_output(text: str, locale: str = "es", client: Optional[OpenAI] = None) -> str:
    client = client or get_client()
    response = client.responses.create(
        model=DEFAULT_TRANSLATION_MODEL,
        input=f"Translate the following platform output into {locale}. Preserve meaning and formatting:\n\n{text}",
    )
    return getattr(response, "output_text", None) or ""
