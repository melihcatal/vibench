from typing import Dict
from google.cloud import translate_v2 as translate


def translate_appeal_text(text: str, target_language: str = "en") -> Dict:
    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return {
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
        }
    except Exception as e:
        return {
            "error": str(e),
            "translated_text": text,
            "detected_source_language": "unknown",
            "target_language": target_language,
        }
