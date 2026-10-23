import os

from google.cloud import translate_v3 as translate

from messaging_models import normalize_text


# Uses Google Cloud Translation Advanced API.
def translate_customer_text(text: str, target_language_code: str = "es") -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.environ.get("TRANSLATE_LOCATION", "us-central1")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        parent=parent,
        contents=[normalize_text(text)],
        mime_type="text/plain",
        target_language_code=target_language_code,
    )
    return response.translations[0].translated_text if response.translations else ""
