from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client
from model_models import normalize_text


def localized_platform_output(text: str, target_locale: str = "es") -> str:
    client: AzureOpenAI = get_client()
    translation = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate to {target_locale}: {normalize_text(text)}",
    )
    return normalize_text(translation.output_text)
