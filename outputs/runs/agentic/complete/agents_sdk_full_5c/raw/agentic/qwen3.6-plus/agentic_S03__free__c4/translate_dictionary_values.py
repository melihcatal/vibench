"""
Translates dictionary values while preserving keys.
Uses Google Cloud Translation API (google.cloud.translate_v2) for translating
dictionary values in batch.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google Neural Machine Translation (NMT)
"""

from typing import Optional, Dict

from translation_client import create_translate_client
from translation_models import (
    DictionaryTranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
    extract_dictionary_values,
    rebuild_translated_dictionary,
    sanitize_text_for_translation,
)


def translate_dictionary_values(
    dictionary: Dict[str, str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, str]:
    """
    Translate dictionary values while preserving the original keys.
    
    Uses the google.cloud.translate_v2 client to batch translate all
    string values in the dictionary via the translate.googleapis.com endpoint.
    Keys are preserved exactly as-is in the returned dictionary.
    
    Args:
        dictionary: Dictionary with string values to translate.
        target_language: Target language code (ISO 639-1).
        source_language: Source language code (ISO 639-1). Auto-detected if None.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
    
    Returns:
        New dictionary with translated values and original keys preserved.
    """
    client = create_translate_client(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    target_lang = normalize_language_code(target_language)
    source_lang = normalize_language_code(source_language) if source_language else None
    
    values_to_translate = extract_dictionary_values(dictionary)
    sanitized_values = [sanitize_text_for_translation(v) for v in values_to_translate]
    non_empty_values = [v for v in sanitized_values if v]
    
    if not non_empty_values:
        return dict(dictionary)
    
    request = DictionaryTranslationRequest(
        dictionary=dictionary,
        source_language=source_lang,
        target_language=target_lang,
    )
    
    translate_kwargs = {
        "values": non_empty_values,
        "target_language": target_lang,
        "format_": "text",
    }
    
    if source_lang:
        translate_kwargs["source_language"] = source_lang
    
    try:
        results = client.translate(**translate_kwargs)
        
        translated_values = []
        if isinstance(results, list):
            for result in results:
                translated = result.get("translatedText", "") if isinstance(result, dict) else result
                translated_values.append(translated)
        
        translated_dict = rebuild_translated_dictionary(dictionary, translated_values)
        
        return translated_dict
    
    except Exception as e:
        raise RuntimeError(f"Google Dictionary Translation API error: {str(e)}")


def translate_dictionary_values_with_response(
    dictionary: Dict[str, str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> TranslationResponse:
    """
    Translate dictionary values and return a full TranslationResponse.
    
    Uses the google.cloud.translate_v2 client via translate.googleapis.com.
    
    Args:
        dictionary: Dictionary with string values to translate.
        target_language: Target language code (ISO 639-1).
        source_language: Source language code (ISO 639-1). Auto-detected if None.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
    
    Returns:
        TranslationResponse containing the translated dictionary result.
    """
    translated_dict = translate_dictionary_values(
        dictionary=dictionary,
        target_language=target_language,
        source_language=source_language,
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    original_values = extract_dictionary_values(dictionary)
    translated_values = [translated_dict.get(k, "") for k in dictionary.keys() if k in translated_dict]
    
    results = []
    for orig, trans in zip(original_values, translated_values):
        results.append(TranslationResult(
            translated_text=trans,
            source_language=source_language or "auto",
            target_language=target_language,
            original_text=orig,
            confidence=1.0,
            model_used="google-translate-v2-nmt",
        ))
    
    return TranslationResponse(
        results=results,
        success=True,
    )


if __name__ == "__main__":
    sample_dict = {
        "greeting": "Hello",
        "farewell": "Goodbye",
        "question": "How are you?",
    }
    result = translate_dictionary_values(sample_dict, target_language="ja")
    for key, value in result.items():
        print(f"{key}: {value}")
