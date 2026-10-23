"""
Translate generated image descriptions using Google Cloud Translation API.
Provider: Google Cloud Translation (translation.googleapis.com)
"""

from typing import List, Optional

from google.cloud import translate_v2 as translate_client

from vision_client import load_image_bytes
from vision_models import ImageDescription, ImageAnalysisPayload
from describe_image import describe_image


def translate_image_description(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    target_language: str = "es",
    source_language: Optional[str] = None,
    vision_model: str = "gpt-4o",
    translation_model: str = "nmt",
) -> dict:
    """
    Generate an image description and translate it using Google Cloud Translation.

    First generates a description using OpenAI GPT-4 Vision, then translates
    it using Google Cloud Translation API (translation.googleapis.com).

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        target_language: Target language code (ISO 639-1, e.g., 'es', 'fr', 'ja').
        source_language: Source language code (optional, auto-detected if None).
        vision_model: OpenAI model for description generation.
        translation_model: Google translation model ('nmt' for Neural Machine Translation).

    Returns:
        Dictionary with original description, translation, and metadata.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)

    description_payload = describe_image(
        image_bytes=raw_image,
        model=vision_model,
    )

    if not description_payload.description:
        return {
            "error": "Failed to generate image description",
            "provider": "openai_vision",
        }

    original_text = description_payload.description.text
    translation_result = translate_text(
        text=original_text,
        target_language=target_language,
        source_language=source_language,
        model=translation_model,
    )

    return {
        "original_text": original_text,
        "translated_text": translation_result["translated_text"],
        "source_language": translation_result.get("detected_source_language", source_language or "auto"),
        "target_language": target_language,
        "vision_provider": "openai",
        "vision_model": vision_model,
        "translation_provider": "google_cloud_translation",
        "translation_model": translation_model,
        "translation_endpoint": "translation.googleapis.com",
    }


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "nmt",
) -> dict:
    """
    Translate text using Google Cloud Translation API.

    Args:
        text: Text to translate.
        target_language: Target language code.
        source_language: Source language code (optional).
        model: Translation model ('nmt' for Neural MT, 'base' for base model).

    Returns:
        Dictionary with translation results.
    """
    client = translate_client.Client()

    translate_kwargs = {
        "target_language": target_language,
        "model": model,
    }

    if source_language:
        translate_kwargs["source_language"] = source_language

    result = client.translate(text, **translate_kwargs)

    return {
        "translated_text": result.get("translatedText", ""),
        "detected_source_language": result.get("detectedSourceLanguage", ""),
        "target_language": result.get("targetLanguage", target_language),
        "model": model,
    }


def translate_alt_text_batch(
    alt_texts: List[str],
    target_languages: List[str],
    model: str = "nmt",
) -> List[dict]:
    """
    Translate multiple alt texts into multiple target languages.

    Args:
        alt_texts: List of alt text strings to translate.
        target_languages: List of target language codes.
        model: Translation model to use.

    Returns:
        List of translation result dictionaries.
    """
    results = []
    client = translate_client.Client()

    for alt_text in alt_texts:
        translations = {}
        for target_lang in target_languages:
            result = client.translate(
                alt_text,
                target_language=target_lang,
                model=model,
            )
            translations[target_lang] = result.get("translatedText", "")

        results.append({
            "original": alt_text,
            "translations": translations,
            "provider": "google_cloud_translation",
            "endpoint": "translation.googleapis.com",
        })

    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = translate_image_description(
            image_path=sys.argv[1],
            target_language="es",
        )
        print(f"Original: {result['original_text']}")
        print(f"Spanish: {result['translated_text']}")
