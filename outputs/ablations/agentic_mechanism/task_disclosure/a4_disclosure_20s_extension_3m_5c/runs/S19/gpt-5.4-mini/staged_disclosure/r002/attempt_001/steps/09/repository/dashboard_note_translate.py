import os
from typing import Optional

import requests


class DashboardNoteTranslator:
    def __init__(self, api_key: Optional[str] = None, endpoint: str = "https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.endpoint = endpoint

    def translate(self, text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
        messages = [
            {"role": "system", "content": "You translate dashboard metric notes accurately and preserve formatting."},
            {"role": "user", "content": self._build_prompt(text, target_locale, source_locale)},
        ]
        response = requests.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def _build_prompt(self, text: str, target_locale: str, source_locale: Optional[str]) -> str:
        parts = [f"Translate the following dashboard note into {target_locale}."]
        if source_locale:
            parts.append(f"Source locale: {source_locale}.")
        parts.append("Preserve metric names, numbers, URLs, and placeholders exactly.")
        parts.append("Return only the translated note.")
        parts.append("")
        parts.append(text)
        return "\n".join(parts)


def translate_dashboard_note(text: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    return DashboardNoteTranslator().translate(text, target_locale, source_locale)
