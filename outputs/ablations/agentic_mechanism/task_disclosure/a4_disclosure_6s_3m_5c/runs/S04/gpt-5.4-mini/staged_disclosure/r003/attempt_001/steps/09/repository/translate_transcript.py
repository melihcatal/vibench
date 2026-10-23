import os
from typing import Any, Dict, List
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def translate_completed_segments(segments: List[Dict[str, Any]], target_lang: str) -> List[Dict[str, Any]]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    texts = [str(segment["text"]) for segment in segments if segment.get("completed") and segment.get("text")]
    if not texts:
        return segments
    response = requests.post(
        DEEPL_API_URL,
        data={
            "auth_key": auth_key,
            "text": texts,
            "target_lang": target_lang,
        },
        timeout=30,
    )
    response.raise_for_status()
    translations = response.json().get("translations", [])
    translated_iter = iter(translations)
    updated = []
    for segment in segments:
        if segment.get("completed") and segment.get("text"):
            translation = next(translated_iter, {})
            new_segment = dict(segment)
            new_segment["translated_text"] = translation.get("text", "")
            updated.append(new_segment)
        else:
            updated.append(dict(segment))
    return updated

