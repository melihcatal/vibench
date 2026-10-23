import os
from google.cloud import translate_v3 as translate
from typing import List


def translate_runbook_notes(
    text_to_translate: List[str],
    target_language_code: str,
    project_id: Optional[str] = None,
) -> List[str]:
    """Translates secret-rotation runbook notes using Google Cloud Translation.

    Args:
        text_to_translate: A list of strings, where each string is a note to translate.
        target_language_code: The BCP-47 language code to translate the text into (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID. If None, it will be inferred from the environment.

    Returns:
        A list of translated strings.
    """
    client = translate.TranslationServiceClient()

    if project_id is None:
        # Attempt to infer project_id from GOOGLE_CLOUD_PROJECT environment variable or default credentials.
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            # In a deployed Google Cloud environment, this is often auto-detected.
            # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set up.
            raise ValueError(
                "Google Cloud project ID must be provided or GOOGLE_CLOUD_PROJECT environment variable set."
            )

    parent = f"projects/{project_id}/locations/global"

    translated_texts = []
    for text in text_to_translate:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    return translated_texts
