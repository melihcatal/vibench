import os
from google.cloud import translate_v2 as translate
from vision_client import get_google_translate_key
from vision_models import TranslationRequest, TranslationResult


def translate_image_description(description: str, target_language: str = "es") -> str:
    """Translate generated image descriptions using Google Cloud Translation API."""
    api_key = get_google_translate_key()

    client = translate.Client(api_key=api_key)

    result = client.translate(
        description, target_language=target_language, source_language="en"
    )

    return result["translatedText"]


def translate_with_request(
    translation_request: TranslationRequest,
) -> TranslationResult:
    """Translate text with a structured request using Google Cloud Translation."""
    api_key = get_google_translate_key()
    client = translate.Client(api_key=api_key)

    result = client.translate(
        translation_request.text,
        target_language=translation_request.target_language,
        source_language=translation_request.source_language,
    )

    return TranslationResult(
        translated_text=result["translatedText"],
        source_language=result.get(
            "detectedSourceLanguage", translation_request.source_language
        ),
        target_language=translation_request.target_language,
    )


if __name__ == "__main__":
    # Example usage
    description = "A beautiful sunset over mountains with a lake in the foreground"

    spanish_translation = translate_image_description(description, "es")
    print(f"Original: {description}")
    print(f"Spanish: {spanish_translation}")

    french_translation = translate_image_description(description, "fr")
    print(f"French: {french_translation}")
