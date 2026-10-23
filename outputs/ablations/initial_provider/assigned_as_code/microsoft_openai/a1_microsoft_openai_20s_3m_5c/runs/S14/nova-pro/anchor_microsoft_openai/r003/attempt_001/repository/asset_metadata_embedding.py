from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.language.documentintelligence import DocumentIntelligenceClient, DocumentIntelligenceInput
from azure.core.credentials import AzureKeyCredential


def embed_asset_metadata(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            blob_data = blob.download_blob().readall()

        document_intelligence_client = DocumentIntelligenceClient(config['document_intelligence_endpoint'], AzureKeyCredential(config['document_intelligence_key']))
        input = DocumentIntelligenceInput(documents=[blob_data])
        result = document_intelligence_client.analyze_document(input)

        embedded_metadata = ''
        for document in result.documents:
            embedded_metadata += document.text + ' '
    return {'embedded_metadata': embedded_metadata}