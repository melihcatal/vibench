from google.cloud import translate_v2 as translate
import json
from typing import Union


def translate_payload(payload: Union[str, dict], target_language: str = "es") -> str:
    client = translate.Client()
    text = payload if isinstance(payload, str) else json.dumps(payload)
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
