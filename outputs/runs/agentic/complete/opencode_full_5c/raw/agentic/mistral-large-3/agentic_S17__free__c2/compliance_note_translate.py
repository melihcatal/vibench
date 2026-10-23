from google.cloud import translate_v2 as translate
import os


def translate_compliance_note(text: str, target_language: str = "es") -> Dict[str, Any]:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
