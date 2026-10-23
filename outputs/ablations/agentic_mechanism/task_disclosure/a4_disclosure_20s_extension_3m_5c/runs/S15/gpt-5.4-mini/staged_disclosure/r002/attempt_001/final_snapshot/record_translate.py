import os
from typing import Any, Dict, Iterable, List, Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def _translate_texts(texts: List[str], target_lang: str, source_lang: Optional[str] = None) -> List[str]:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    data = [("text", text) for text in texts]
    data.append(("target_lang", target_lang))
    if source_lang:
        data.append(("source_lang", source_lang))

    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data=data,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return [item["text"] for item in payload["translations"]]


def translate_record(record: Dict[str, Any], target_lang: str, fields: Optional[Iterable[str]] = None, source_lang: Optional[str] = None) -> Dict[str, Any]:
    field_names = list(fields) if fields is not None else [
        key for key, value in record.items() if isinstance(value, str) and value.strip()
    ]
    texts = [record[name] for name in field_names if isinstance(record.get(name), str)]
    translated = _translate_texts(texts, target_lang=target_lang, source_lang=source_lang)

    updated = dict(record)
    for name, value in zip(field_names, translated):
        updated[name] = value
    return updated


def translate_records(records: List[Dict[str, Any]], target_lang: str, fields: Optional[Iterable[str]] = None, source_lang: Optional[str] = None) -> List[Dict[str, Any]]:
    return [translate_record(record, target_lang=target_lang, fields=fields, source_lang=source_lang) for record in records]
