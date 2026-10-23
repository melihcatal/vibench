from google.cloud import translate_v2 as translate
from typing import Dict, Optional

def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, str]:
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result.get("detectedSourceLanguage")
    }