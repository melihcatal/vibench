import os
from google.cloud import translate_v2 as translate
from.storage_client import get_storage_client

def stored_text_translate(container_name, blob_name, target_language):
    blob_service_client = get_storage_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_stream = blob_client.download_blob()
    text = download_stream.readall().decode('utf-8')
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']