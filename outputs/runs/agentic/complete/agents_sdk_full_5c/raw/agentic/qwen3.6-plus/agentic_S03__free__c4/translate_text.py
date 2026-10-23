"""
Translates a single text string between languages.
Uses Google Cloud Translation API (google.cloud.translate_v2) for translation.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google Neural Machine Translation (NMT)
"""

from typing import Optional

from translation_client import create_translate_client
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
    sanitize_text_for_translation,
)


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> TranslationResponse:
    """
    Translate a single text string between languages using Google Cloud Translation API.
    
    Uses the google.cloud.translate_v2 client to perform translation
    via the translate.googleapis.com endpoint.
    
    Args:
        text: The text string to translate.
        target_language: Target language code (ISO 639-1).
        source_language: Source language code (ISO 639-1). Auto-detected if None.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
    
    Returns:
        TranslationResponse with the translated text and metadata.
    """
    client = create_translate_client(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    sanitized_text = sanitize_text_for_translation(text)
    target_lang = normalize_language_code(target_language)
    source_lang = normalize_language_code(source_language) if source_language else None
    
    request = TranslationRequest(
        text=sanitized_text,
        source_language=source_lang,
        target_language=target_lang,
        format_type="text",
        model="nmt",
    )
    
    translate_kwargs = {
        "values": [sanitized_text],
        "target_language": target_lang,
        "format_": "text",
    }
    
    if source_lang:
        translate_kwargs["source_language"] = source_lang
    
    try:
        result = client.translate(**translate_kwargs)
        
        translated = result.get("translatedText", "") if isinstance(result, dict) else result
        detected_source = result.get("detectedSourceLanguage", source_lang or "unknown")
        
        translation_result = TranslationResult(
            translated_text=translated,
            source_language=detected_source,
            target_language=target_lang,
            original_text=sanitized_text,
            confidence=1.0,
            model_used="google-translate-v2-nmt",
        )
        
        return TranslationResponse(
            results=[translation_result],
            success=True,
        )
    
    except Exception as e:
        return TranslationResponse(
            results=[],
            success=False,
            error_message=f"Google Translation API error: {str(e)}",
        )


if __name__ == "__main__":
    response = translate_text("Hello, world!", target_language="es")
    if response.success:
        print(response.results[0].translated_text)
