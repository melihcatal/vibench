from azure.ai.translation.document import DocumentTranslationClient

def stored_text_translate(container_name: str, blob_name: str, target_language: str):
    client = StorageClient()
    blob_client = client.get_blob_client(container_name, blob_name)
    document_translation_client = DocumentTranslationClient()
    result = document_translation_client.translate_document(blob_client.url, target_language)
    return result.translated_text