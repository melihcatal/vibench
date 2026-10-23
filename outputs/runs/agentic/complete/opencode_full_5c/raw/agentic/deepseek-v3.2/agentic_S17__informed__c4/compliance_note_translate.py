import os
from security_models import TranslationResult
from google.cloud import translate_v2 as translate


def translate_compliance_notes(
    text: str, target_language: str = "es"
) -> TranslationResult:
    """
    Translate encryption or compliance notes for reviewers using Google Cloud Translation.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        return TranslationResult(
            success=False,
            error="GOOGLE_APPLICATION_CREDENTIALS environment variable is required",
            provider="google_translate",
        )

    try:
        client = translate.Client()

        result = client.translate(text, target_language=target_language)

        return TranslationResult(
            success=True,
            translated_text=result["translatedText"],
            source_lang=result.get("detectedSourceLanguage", "en"),
            target_lang=target_language,
            provider="google_translate",
        )

    except Exception as e:
        return TranslationResult(
            success=False, error=str(e), provider="google_translate"
        )
