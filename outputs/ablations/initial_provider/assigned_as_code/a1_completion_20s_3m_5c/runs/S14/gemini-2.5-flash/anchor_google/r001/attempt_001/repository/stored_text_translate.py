from google.cloud import translate
from storage_client import get_project_id

def stored_text_translate(text_to_translate: str, target_language_code: str = "es"):
    client = translate.TranslationServiceClient()

    parent = f"projects/{get_project_id()}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    for translation in response.translations:
        return {"translated_text": translation.translated_text}
    return {"translated_text": ""}
