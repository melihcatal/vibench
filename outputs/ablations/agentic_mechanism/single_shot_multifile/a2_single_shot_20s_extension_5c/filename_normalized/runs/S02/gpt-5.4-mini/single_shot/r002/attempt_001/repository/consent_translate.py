import os
from typing import Any

import requests

DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")


def translate_consent_copy(text: str, target_lang: str, source_lang: str | None = None) -> dict[str, Any]:
    data = {"text": text, "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang
    headers = {"Authorization": f"DeepL-Auth-Key {os.getenv('DEEPL_AUTH_KEY', '')}"}
    response = requests.post(DEEPL_API_URL, data=data, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
