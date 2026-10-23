import os
import requests
from typing import Dict, Any, List

def translate_record_fields(record: Dict[str, Any], target_lang: str = "EN", fields: List[str] | None = None) -> Dict[str, Any]:
    if fields is None:
        fields = ["title", "description", "content"]  # common user-facing fields
    
    api_key = os.environ["DEEPL_API_KEY"]
    translated = record.copy()
    
    for field in fields:
        if field in record and isinstance(record[field], str) and record[field].strip():
            resp = requests.post(
                "https://api-free.deepl.com/v2/translate",
                auth=(api_key, ""),
                data={
                    "text": record[field],
                    "target_lang": target_lang.upper()
                },
            )
            if resp.status_code == 200:
                translated[field] = resp.json()["translations"][0]["text"]
    
    return translated