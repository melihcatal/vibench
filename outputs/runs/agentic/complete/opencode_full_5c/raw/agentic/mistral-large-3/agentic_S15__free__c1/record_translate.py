from typing import Any, Dict, List
import requests
import os


def translate_records(
    records: List[Dict[str, Any]], target_language: str = "es"
) -> List[Dict[str, Any]]:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"

    translations = []
    for record in records:
        document = record.get("document", {})
        text = document.get("content", "")

        payload = {"q": text, "target": target_language}

        response = requests.post(url, json=payload)
        response.raise_for_status()
        translation = response.json()

        translations.append(
            {
                "id": record["id"],
                "partition_key": record["partition_key"],
                "translated_content": translation.get("data", {})
                .get("translations", [{}])[0]
                .get("translatedText", ""),
            }
        )

    return translations
