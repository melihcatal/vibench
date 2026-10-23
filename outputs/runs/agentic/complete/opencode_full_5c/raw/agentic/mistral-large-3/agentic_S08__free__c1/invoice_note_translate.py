from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    if not text:
        return {"translated_text": "", "detected_language": "", "error": None}

    client = translate.Client()
    result = {"translated_text": "", "detected_language": "", "error": None}

    try:
        detection = client.detect_language(text)
        result["detected_language"] = detection["language"]

        if detection["language"] != target_language:
            translation = client.translate(text, target_language=target_language)
            result["translated_text"] = translation["translatedText"]
        else:
            result["translated_text"] = text

    except Exception as e:
        result["error"] = str(e)

    return result
