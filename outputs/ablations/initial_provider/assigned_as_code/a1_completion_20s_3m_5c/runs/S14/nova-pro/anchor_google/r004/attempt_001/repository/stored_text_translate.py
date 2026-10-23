from google.cloud import storage
from storage_client import get_storage_client
from google.cloud import translate


def stored_text_translate(payload):
    client = get_storage_client()
    blob = client.bucket(payload["bucket"]).blob(payload["object_name"])
    content = blob.download_as_text()
    translate_client = translate.TranslationServiceClient()
    response = translate_client.translate_text(content, target_language_code=payload["target_language"])
    translated_text = response.translations[0].translated_text
    return {"translated_text": translated_text}