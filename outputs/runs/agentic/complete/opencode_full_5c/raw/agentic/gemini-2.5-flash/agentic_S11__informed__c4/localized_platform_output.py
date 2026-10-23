from google.cloud import translate_v3 as translate
import os
from model_models import TranslatedText


def localized_platform_output(
    text: str, target_language: str, project_id: str = None
) -> TranslatedText:
    """Translates platform model output for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID. If None, it will try to get it from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        A TranslatedText object containing the translated text, source, and target languages.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    source_language = response.translations[0].detected_language_code

    return TranslatedText(
        text=translated_text,
        source_language=source_language,
        target_language=target_language,
    )
