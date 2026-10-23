import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_payload(
    payload: Dict[str, Any], target_lang: str = "en"
) -> Dict[str, Any]:
    """Translate text fields inside a message payload to the target language.

    Uses Google Cloud Translation API.
    Only strings under the top-level \"text\" key are translated.
    """
    client = translate.Client()
    # Find all string values at any depth; here we just handle the top-level
    if "text" in payload:
        original = payload["text"]
        try:
            result = client.translate(original, target_language=target_lang)
            payload["text"] = result["translatedText"]
        except Exception as e:
            raise RuntimeError(f"Translation error: {e}")
    return payload
