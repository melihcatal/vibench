from google.cloud import translate
import os


def translate_compliance_note(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Or pass as argument
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    # Assuming only one text content is sent for translation
    if response.translations:
        return response.translations[0].translated_text
    return ""
