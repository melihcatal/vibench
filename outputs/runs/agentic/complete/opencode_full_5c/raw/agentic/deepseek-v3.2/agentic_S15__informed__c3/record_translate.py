import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate


def translate_text_fields(
    texts: List[str], target_language: str = "en", source_language: str = None
) -> Dict[str, Any]:
    """
    Translate user-facing document fields using Google Cloud Translation.

    Args:
        texts: List of text strings to translate
        target_language: Target language code (e.g., "en", "es", "fr")
        source_language: Source language code (optional, auto-detected if not provided)

    Returns:
        dict: Translation results
    """
    try:
        # Google Cloud Translation configuration
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
            )

        # Initialize Google Cloud Translation client
        client = translate.Client()

        translations = []
        detected_languages = []

        for text in texts:
            # Call Google Cloud Translation API
            if source_language:
                result = client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language,
                )
            else:
                result = client.translate(text, target_language=target_language)

            translations.append(
                {
                    "original_text": text[:200] + "..." if len(text) > 200 else text,
                    "translated_text": result["translatedText"],
                    "source_language": result.get(
                        "detectedSourceLanguage", source_language
                    ),
                    "target_language": target_language,
                    "original_length": len(text),
                    "translated_length": len(result["translatedText"]),
                }
            )

            if "detectedSourceLanguage" in result:
                detected_languages.append(result["detectedSourceLanguage"])

        # Calculate language statistics
        language_stats = {}
        for lang in detected_languages:
            language_stats[lang] = language_stats.get(lang, 0) + 1

        return {
            "success": True,
            "translations": translations,
            "statistics": {
                "total_texts": len(texts),
                "target_language": target_language,
                "source_language": source_language or "auto-detected",
                "detected_languages": language_stats,
                "average_translation_ratio": sum(
                    t["translated_length"] / max(1, t["original_length"])
                    for t in translations
                )
                / len(translations)
                if translations
                else 0,
            },
            "provider": "Google Cloud Translation",
            "service": "translate.googleapis.com",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "total_texts": len(texts) if "texts" in locals() else 0,
            "target_language": target_language,
            "provider": "Google Cloud Translation",
        }
