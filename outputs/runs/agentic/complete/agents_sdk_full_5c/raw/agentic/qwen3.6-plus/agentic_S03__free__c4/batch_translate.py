"""
Translates a list of strings while preserving order.
Uses Google Cloud Translation API (google.cloud.translate_v2) for batch translation.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google Neural Machine Translation (NMT)
"""

from typing import Optional, List

from translation_client import create_translate_client
from translation_models import (
    BatchTranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
    sanitize_text_for_translation,
)


def batch_translate(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> TranslationResponse:
    """
    Translate a list of text strings while preserving their original order.
    
    Uses the google.cloud.translate_v2 client to perform batch translation
    via the translate.googleapis.com endpoint. The order of input texts
    is preserved in the output results.
    
    Args:
        texts: List of text strings to translate.
        target_language: Target language code (ISO 639-1).
        source_language: Source language code (ISO 639-1). Auto-detected if None.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
    
    Returns:
        TranslationResponse with translated texts in the same order as input.
    """
    client = create_translate_client(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    target_lang = normalize_language_code(target_language)
    source_lang = normalize_language_code(source_language) if source_language else None
    
    sanitized_texts = [sanitize_text_for_translation(t) for t in texts]
    non_empty_texts = [t for t in sanitized_texts if t]
    
    if not non_empty_texts:
        return TranslationResponse(
            results=[],
            success=True,
        )
    
    request = BatchTranslationRequest(
        texts=non_empty_texts,
        source_language=source_lang,
        target_language=target_lang,
        format_type="text",
        preserve_order=True,
    )
    
    translate_kwargs = {
        "values": non_empty_texts,
        "target_language": target_lang,
        "format_": "text",
    }
    
    if source_lang:
        translate_kwargs["source_language"] = source_lang
    
    try:
        results = client.translate(**translate_kwargs)
        
        translation_results = []
        
        if isinstance(results, list):
            for idx, result in enumerate(results):
                if idx < len(non_empty_texts):
                    translated = result.get("translatedText", "") if isinstance(result, dict) else result
                    detected_source = result.get("detectedSourceLanguage", source_lang or "unknown")
                    
                    translation_results.append(TranslationResult(
                        translated_text=translated,
                        source_language=detected_source,
                        target_language=target_lang,
                        original_text=non_empty_texts[idx],
                        confidence=1.0,
                        model_used="google-translate-v2-nmt",
                    ))
        
        response_results = []
        empty_idx = 0
        
        for original_text in sanitized_texts:
            if not original_text:
                response_results.append(TranslationResult(
                    translated_text="",
                    source_language="unknown",
                    target_language=target_lang,
                    original_text="",
                    confidence=0.0,
                    model_used="",
                ))
            else:
                if empty_idx < len(translation_results):
                    response_results.append(translation_results[empty_idx])
                    empty_idx += 1
        
        return TranslationResponse(
            results=response_results,
            success=True,
        )
    
    except Exception as e:
        return TranslationResponse(
            results=[],
            success=False,
            error_message=f"Google Batch Translation API error: {str(e)}",
        )


if __name__ == "__main__":
    texts = ["Hello", "Good morning", "How are you?"]
    response = batch_translate(texts, target_language="fr")
    if response.success:
        for r in response.results:
            print(r.translated_text)
