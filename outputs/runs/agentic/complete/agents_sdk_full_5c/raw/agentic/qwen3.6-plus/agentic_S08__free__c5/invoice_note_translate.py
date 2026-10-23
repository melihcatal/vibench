"""
Translate extracted invoice notes or descriptions using DeepL Translation API.
Provider: DeepL API (deepl translator service)
"""

import os
import json
from typing import Optional, List
import deepl

from document_models import TranslationResult


def translate_invoice_note(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TranslationResult:
    """
    Translate extracted invoice notes, descriptions, or memo fields using DeepL API.
    
    Uses the DeepL translation service (api.deepl.com) to translate vendor
    notes, invoice descriptions, or other extracted text fields into the target language.
    
    Supported target languages include: EN, DE, FR, ES, PT, IT, NL, PL, RU, JA, ZH, KO, BG, etc.
    
    Args:
        text: Invoice note or description text to translate
        target_language: Target language code (e.g., 'EN', 'DE', 'FR')
        source_language: Source language code (optional, DeepL auto-detects if not provided)
        api_key: DeepL API key
    
    Returns:
        TranslationResult with translated text and metadata
    """
    deepl_api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    
    if not deepl_api_key:
        raise ValueError("DeepL API key must be provided via parameter or DEEPL_API_KEY env var")
    
    translator = deepl.Translator(deepl_api_key)
    
    try:
        source_lang_code = source_language.upper() if source_language else None
        target_lang_code = target_language.upper()
        
        result = translator.translate_text(
            text,
            source_lang=source_lang_code,
            target_lang=target_lang_code,
        )
        
        detected_source = result.detected_source_lang if hasattr(result, "detected_source_lang") else source_language
        
        return TranslationResult(
            source_text=text,
            source_language=detected_source,
            target_text=result.text,
            target_language=target_lang_code,
            confidence=1.0,
        )
    
    except deepl.exceptions.DeepLException as e:
        raise RuntimeError(f"DeepL translation failed: {e}") from e


def translate_invoice_notes_batch(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[TranslationResult]:
    """
    Translate multiple invoice notes in a single DeepL API call.
    
    Args:
        texts: List of invoice note/description texts to translate
        target_language: Target language code (e.g., 'EN', 'DE', 'FR')
        source_language: Source language code (optional)
        api_key: DeepL API key
    
    Returns:
        List of TranslationResult objects
    """
    deepl_api_key = api_key or os.environ.get("DEEPL_API_KEY", "")
    
    if not deepl_api_key:
        raise ValueError("DeepL API key must be provided via parameter or DEEPL_API_KEY env var")
    
    translator = deepl.Translator(deepl_api_key)
    
    try:
        source_lang_code = source_language.upper() if source_language else None
        target_lang_code = target_language.upper()
        
        results = translator.translate_text(
            texts,
            source_lang=source_lang_code,
            target_lang=target_lang_code,
        )
        
        translations: List[TranslationResult] = []
        for i, result in enumerate(results):
            detected_source = result.detected_source_lang if hasattr(result, "detected_source_lang") else source_language
            translations.append(
                TranslationResult(
                    source_text=texts[i],
                    source_language=detected_source,
                    target_text=result.text,
                    target_language=target_lang_code,
                    confidence=1.0,
                )
            )
        
        return translations
    
    except deepl.exceptions.DeepLException as e:
        raise RuntimeError(f"DeepL batch translation failed: {e}") from e


if __name__ == "__main__":
    sample_text = "Rechnung für Büromaterial, Lieferung am 15. Januar."
    
    try:
        result = translate_invoice_note(sample_text, target_language="EN")
        print(result.model_dump_json(indent=2))
    except ValueError as e:
        print(f"Skipping translation demo (no API key): {e}")
