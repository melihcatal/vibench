from typing import Any, Dict

import requests


def alt_text_translate(text: str, target_language: str = "es") -> str:
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": __import__("os").getenv("GOOGLE_TRANSLATE_API_KEY")},
        json={"q": text, "target": target_language, "format": "text"},
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data.get("data", {}).get("translations", [{}])[0].get("translatedText", "")
