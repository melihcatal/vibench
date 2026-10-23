from google.cloud import translate_v3 as translate
import os


def translate_text(
    text: str,
    target_language: str = "en",
    project_id: str = os.environ.get("GOOGLE_CLOUD_PROJECT"),
) -> str:
    """
    Translates text using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text
