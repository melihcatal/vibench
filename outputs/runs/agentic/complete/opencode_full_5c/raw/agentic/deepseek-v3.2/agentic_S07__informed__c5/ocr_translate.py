import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from document_models import TranslationRequest, TranslationResult


def translate_ocr_text(
    text: str, target_language: str = "es", source_language: str = "en"
) -> TranslationResult:
    """Translate extracted OCR text using Azure AI Translator."""
    endpoint = os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "global")

    if not key:
        raise ValueError("Please set AZURE_TRANSLATOR_KEY environment variable")

    credential = AzureKeyCredential(key)
    client = TextTranslationClient(
        credential=credential, region=region, endpoint=endpoint
    )

    response = client.translate(
        body=[text], to_language=[target_language], from_language=source_language
    )

    if not response or not response[0].translations:
        raise ValueError("Translation failed")

    translation = response[0].translations[0]

    return TranslationResult(
        translated_text=translation.text,
        source_language=source_language,
        target_language=target_language,
        confidence=getattr(translation, "confidence", None),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python ocr_translate.py <text> [target_language] [source_language]"
        )
        print("Example: python ocr_translate.py 'Hello world' es en")
        sys.exit(1)

    text = sys.argv[1]
    target_lang = sys.argv[2] if len(sys.argv) > 2 else "es"
    source_lang = sys.argv[3] if len(sys.argv) > 3 else "en"

    result = translate_ocr_text(text, target_lang, source_lang)
    print(f"Original ({result.source_language}): {text}")
    print(f"Translated ({result.target_language}): {result.translated_text}")
    if result.confidence:
        print(f"Confidence: {result.confidence}")
