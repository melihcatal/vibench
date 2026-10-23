import os
from google.cloud import translate_v2 as translate


def translate_onboarding_copy(
    text: str, target_language: str, project_id: str | None = None
) -> str:
    # Google Cloud Translation API client initialization
    # The client will automatically pick up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS or GCLOUD_PROJECT)
    translate_client = translate.Client(
        project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    )

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Translate the text
    result = translate_client.translate(text, target_language=target_language)

    # The result contains the translated text and the detected source language.
    # We only return the translated text.
    return result["translatedText"]
