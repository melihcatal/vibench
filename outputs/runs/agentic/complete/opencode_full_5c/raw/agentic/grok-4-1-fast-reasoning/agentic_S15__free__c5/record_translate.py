import os
import requests
from typing import Dict, Any, List


def translate_record_fields(
    record: Dict[str, Any], fields: List[str], target_lang: str = "EN"
) -> Dict[str, Any]:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY required")

    translated_record = record.copy()
    url = "https://api-free.deepl.com/v2/translate"

    for field in fields:
        text = record.get(field, "")
        if not text:
            continue
        data = {"text": [text], "target_lang": target_lang}
        headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        translated = response.json()["translations"][0]["text"]
        translated_record[field] = translated

    return translated_record
