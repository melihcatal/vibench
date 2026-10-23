from google.cloud import translate_v3 as translate
import os

# Initialize Google Cloud Translation client
# The client automatically uses GOOGLE_APPLICATION_CREDENTIALS environment variable
# or other default credentials mechanisms.
client = translate.TranslationServiceClient()

def translate_text(text: str, target_language_code: str, project_id: str = None) -> dict:
    """
    Translates the given text into the target language using Google Cloud Translation.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            return {"error": "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set."}

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({"translatedText": translation.translated_text})

    if translations:
        return {"translations": translations, "message": "Text translated successfully"}
    else:
        return {"error": "No translations found."}
