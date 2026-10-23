import os
from google.cloud import translate


def translate_text(
    text: str, target_language: str = "es", project_id: str = None
) -> dict:
    if project_id is None:
        # GOOGLE_APPLICATION_CREDENTIALS should be set, and project ID can often be inferred
        # However, for explicit usage, project_id might be needed if not inferred
        # In a real scenario, you might get this from an environment variable or config.
        # For this example, we'll assume it can be inferred or handle a missing project_id gracefully.
        pass

    client = translate.TranslationServiceClient()

    # The location must be a global one, for example, global, us-central1, etc.
    # For basic translation, 'global' is generally sufficient.
    location = "global"

    parent = (
        f"projects/{project_id}/locations/{location}"
        if project_id
        else f"projects/-/locations/{location}"
    )

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    return {"translated_text": translations[0] if translations else None}
