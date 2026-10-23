from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.core.credentials import AzureKeyCredential


def translate_stored_text(object_name, target_language, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            blob_data = blob.download_blob().readall()

        document_translation_client = DocumentTranslationClient(config['translation_endpoint'], AzureKeyCredential(config['translation_key']))
        input = DocumentTranslationInput(
            source_url=blob.url,
            target_language_code=target_language,
            source_language_code='en'
        )
        poller = document_translation_client.begin_translate_document(input)
        result = poller.result()

        translated_text = ''
        for document in result.translated_documents:
            translated_text += document.content
    return {'translated_text': translated_text}