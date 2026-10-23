import os
import sys
from typing import List

import requests


DEepl_API_URL = "https://api-free.deepl.com/v2/translate"


def batch_translate_texts(texts: List[str], source_language: str, target_language: str) -> List[str]:
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    response = requests.post(
        DEepl_API_URL,
        data={
            "auth_key": api_key,
            "text": texts,
            "source_lang": source_language,
            "target_lang": target_language,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if len(translations) != len(texts):
        raise RuntimeError("Unexpected number of translations returned by DeepL")
    return [item["text"] for item in translations]


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: batch_translate.py <source_language> <target_language> <text1> [<text2> ...]"
        )
    source_language = sys.argv[1]
    target_language = sys.argv[2]
    texts = sys.argv[3:]
    for translated in batch_translate_texts(texts, source_language, target_language):
        print(translated)


if __name__ == "__main__":
    main()
