"""
Translate a list of strings while preserving order using Google Cloud Translation API v3.
"""
from typing import List, Dict, Optional
from translation_client import create_default_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(
    texts: List[str],
    target_language: str,
    source_language: str = None,
    format: str = "text",
    preserve_order: bool = True,
) -> Dict[str, list]:
    """
    Translate a list of strings while preserving their original order.
    
    Uses Google Cloud Translation v3 API (translate.googleapis.com) which
    returns translations in the same order as the input contents array.
    The Google NMT model is used for neural machine translation.
    
    Args:
        texts: List of strings to translate
        target_language: Target language code (e.g., 'fr', 'ja')
        source_language: Source language code (optional, auto-detected if not provided)
        format: Content format ('text' or 'html')
        preserve_order: Whether to maintain input order in output (default True)
    
    Returns:
        Dictionary with 'translations' list and 'source_language' detected
    """
    if not texts:
        return {"translations": [], "source_language": "auto"}

    request = BatchTranslationRequest(
        texts=texts,
        target_language=target_language,
        source_language=source_language,
        format=format,
    )

    client = create_default_client()
    mime_type = "text/html" if request.format == "html" else "text/plain"

    response = client.batch_translate(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
        mime_type=mime_type,
    )

    if preserve_order:
        translations_list = []
        for item in response.translations:
            translations_list.append(item.translated_text)
    else:
        translations_list = [t.translated_text for t in response.translations]

    return {
        "translations": translations_list,
        "source_language": response.translations[0].source_language if response.translations else "auto",
        "total_characters": response.total_characters,
        "count": len(translations_list),
    }


if __name__ == "__main__":
    texts_to_translate = [
        "Welcome to our service.",
        "Please select your preferences.",
        "Your account has been created.",
    ]
    
    result = batch_translate(
        texts=texts_to_translate,
        target_language="de",
        source_language="en",
    )
    for i, translation in enumerate(result["translations"]):
        print(f"  {texts_to_translate[i]} -> {translation}")
