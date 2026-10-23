from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.translation.document import DocumentTranslationClient
from azure.ai.translation.document.models import DocumentTranslationInput



def translate_stored_text(config, object_name, target_language):
    with DefaultAzureCredential() as credential:
        storage_client = BlobServiceClient(config['account_url'], credential=credential)
        blob = storage_client.get_blob_client(container=config['container'], blob=object_name)
        image_data = blob.download_blob().readall()

        translation_client = DocumentTranslationClient(endpoint=config['translation_endpoint'], credential=credential)
        input = DocumentTranslationInput(source_url=blob.url, target_language_code=target_language)
        result = translation_client.translate_document(input)

        if result.status == 'Succeeded':
            return {'translated_text': result.translated_document_url}
        else:
            return {'error': 'Translation failed'}