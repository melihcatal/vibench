from __future__ import annotations

import os
from typing import Dict

from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
SAFETY_MODEL = os.getenv("AZURE_OPENAI_SAFETY_MODEL", "gpt-4o-mini")


class PlatformOutputSafety:
    def __init__(self):
        self.client = AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT or None, api_key=AZURE_OPENAI_API_KEY or None, api_version=AZURE_OPENAI_API_VERSION)

    def check(self, text: str) -> Dict[str, object]:
        prompt = f"Assess whether the following output is unsafe. Return JSON with keys unsafe and reason. Output: {text}"
        result = self.client.chat.completions.create(model=SAFETY_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0)
        content = result.choices[0].message.content or ""
        return {"provider": "azure-openai", "model": SAFETY_MODEL, "result": content}
