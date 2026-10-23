import os
from google.cloud import translate_v3 as translate


def translate_caption(text, target_language_code="es"):
    client = translate.TranslationServiceClient()
    project_id = os.getenv(
        "GOOGLE_CLOUD_PROJECT"
    )  # GOOGLE_APPLICATION_CREDENTIALS for auth
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
