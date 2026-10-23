from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v3 as translate


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = translate.TranslationServiceClient()
    parent = client.common_location_path(os.getenv("GOOGLE_CLOUD_PROJECT", "default-project"), "global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
            "source_language_code": source_language or "",
        }
    )
    return response.translations[0].translated_text


if __name__ == "__main__":
    print(translate_script("Hello world", "es"))
