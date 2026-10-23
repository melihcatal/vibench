import boto3
from typing import Optional, List
from storage_models import TranslateRequest, TranslateResponse


def translate_text(
    text: str, source_language_code: str = "auto", target_language_code: str = "en"
) -> TranslateResponse:
    """
    Translate text using AWS Translate service.

    Args:
        text: Text to translate
        source_language_code: Source language code (default: "auto" for auto-detection)
        target_language_code: Target language code (default: "en" for English)

    Returns:
        TranslateResponse with translated text
    """
    if not text or not text.strip():
        return TranslateResponse(
            success=False,
            error_message="No text provided for translation",
            provider="aws_translate",
        )

    try:
        # Initialize Translate client
        translate_client = boto3.client("translate")

        # Prepare translation parameters
        params = {
            "Text": text,
            "SourceLanguageCode": source_language_code,
            "TargetLanguageCode": target_language_code,
        }

        # Call AWS Translate
        response = translate_client.translate_text(**params)

        return TranslateResponse(
            success=True,
            translated_text=response["TranslatedText"],
            source_language_code=response.get(
                "SourceLanguageCode", source_language_code
            ),
            target_language_code=target_language_code,
            provider="aws_translate",
        )

    except Exception as e:
        return TranslateResponse(
            success=False, error_message=str(e), provider="aws_translate"
        )


def translate_document_text(
    extracted_text: str, target_language: str = "en"
) -> TranslateResponse:
    """
    Translate text extracted from a stored document.

    Args:
        extracted_text: Text extracted from document (via OCR or other means)
        target_language: Target language code (default: "en" for English)

    Returns:
        TranslateResponse with translated text
    """
    # Auto-detect source language
    return translate_text(extracted_text, "auto", target_language)


def batch_translate_texts(
    texts: List[str],
    source_language_code: str = "auto",
    target_language_code: str = "en",
) -> List[TranslateResponse]:
    """
    Translate multiple texts in batch.

    Args:
        texts: List of texts to translate
        source_language_code: Source language code
        target_language_code: Target language code

    Returns:
        List of TranslateResponse objects
    """
    results = []

    for text in texts:
        if text and text.strip():
            result = translate_text(text, source_language_code, target_language_code)
        else:
            result = TranslateResponse(
                success=False, error_message="Empty text", provider="aws_translate"
            )
        results.append(result)

    return results


def get_supported_languages() -> List[dict]:
    """
    Get list of languages supported by AWS Translate.

    Returns:
        List of language dictionaries with code and name
    """
    try:
        translate_client = boto3.client("translate")

        # Get supported languages
        response = translate_client.list_languages()

        languages = []
        for lang in response.get("Languages", []):
            languages.append(
                {"code": lang["LanguageCode"], "name": lang.get("LanguageName", "")}
            )

        return languages

    except Exception as e:
        print(f"Error getting supported languages: {e}")
        return []


def detect_language(text: str) -> dict:
    """
    Detect the language of the given text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with language code and confidence score
    """
    if not text or not text.strip():
        return {"code": "unknown", "confidence": 0.0}

    try:
        translate_client = boto3.client("translate")

        response = translate_client.translate_text(
            Text=text[:100],  # Use first 100 chars for detection
            SourceLanguageCode="auto",
            TargetLanguageCode="en",  # Target doesn't matter for detection
        )

        return {
            "code": response.get("SourceLanguageCode", "unknown"),
            "confidence": 1.0,  # AWS doesn't provide confidence score in response
        }

    except Exception as e:
        print(f"Error detecting language: {e}")
        return {"code": "unknown", "confidence": 0.0}


if __name__ == "__main__":
    # Example usage
    request = TranslateRequest(
        text="Bonjour, comment allez-vous? Je m'appelle Pierre.",
        source_language_code="auto",
        target_language_code="en",
    )
    result = translate_text(
        request.text, request.source_language_code, request.target_language_code
    )
    print(f"Translation result: {result.success}")
    if result.success:
        print(f"Original text: {request.text}")
        print(f"Translated text: {result.translated_text}")
        print(f"Source language: {result.source_language_code}")
        print(f"Target language: {result.target_language_code}")

    # Example with document text
    document_text = (
        "Este es un documento importante que necesita ser traducido al inglés."
    )
    doc_result = translate_document_text(document_text, "en")
    print(f"\nDocument translation: {doc_result.success}")
    if doc_result.success:
        print(f"Translated: {doc_result.translated_text}")
