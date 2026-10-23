from typing import Any, Dict

from document_client import translate_client


def translate_ocr_text(text: str, target_language_code: str = "en") -> Dict[str, Any]:
    client = translate_client()
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode"), "target_language": target_language_code, "raw": response}
