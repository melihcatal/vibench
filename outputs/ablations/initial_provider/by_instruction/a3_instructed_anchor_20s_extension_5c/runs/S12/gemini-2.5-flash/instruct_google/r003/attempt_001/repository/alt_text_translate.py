from google.cloud import translate_v3 as translate
import os

def translate_alt_text(text: str, target_language_code: str = 'es') -> str:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        return "Error: GCP_PROJECT_ID environment variable not set for translation."

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en", # Assuming source is English based on previous steps
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, but we only sent one text
    if response.translations:
        return response.translations[0].translated_text
    else:
        return "Translation failed."
