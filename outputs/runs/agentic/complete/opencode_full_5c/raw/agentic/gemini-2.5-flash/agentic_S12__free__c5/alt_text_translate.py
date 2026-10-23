import os
from vision_client import get_translation_client
from google.cloud.translate_v3 import TranslateTextRequest


def translate_alt_text(
    text: str, target_language: str = "es", project_id: str = None
) -> str:
    client = get_translation_client()

    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
        )

    parent = f"projects/{project_id}/locations/global"
    request = TranslateTextRequest(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    response = client.translate_text(request=request)

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables are set.
    sample_alt_text = "A brown dog playing in a field."
    target_lang = "fr"
    translated_text = translate_alt_text(sample_alt_text, target_lang)
    print(f"Original: {sample_alt_text}")
    print(f"Translated ({target_lang}): {translated_text}")
