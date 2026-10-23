from __future__ import annotations

import os

from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
TRANSLATION_MODEL = os.getenv("AZURE_OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def localized_platform_output(text: str, target_locale: str = "es") -> str:
    client = AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT or None, api_key=AZURE_OPENAI_API_KEY or None, api_version=AZURE_OPENAI_API_VERSION)
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[{"role": "system", "content": f"Translate to {target_locale}."}, {"role": "user", "content": text}],
        temperature=0,
    )
    return response.choices[0].message.content or ""
