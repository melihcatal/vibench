import os

from google.cloud import translate_v3 as translate


def translate_script(text, target_language, parent=None):
    client = translate.TranslationServiceClient()
    project = parent or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    response = client.translate_text(
        parent=f"projects/{project}/locations/{location}",
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return response.translations[0].translated_text if response.translations else ""
