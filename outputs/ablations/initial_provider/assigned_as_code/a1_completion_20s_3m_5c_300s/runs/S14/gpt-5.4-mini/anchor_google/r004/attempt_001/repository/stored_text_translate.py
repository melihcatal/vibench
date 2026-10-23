from google.cloud import translate_v2 as translate

from storage_client import get_blob_client


def stored_text_translate(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    text = blob.download_as_text()
    client = translate.Client()
    result = client.translate(text, target_language=payload["target_language"])
    return {"translated_text": result["translatedText"]}
