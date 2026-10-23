from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


def extract_text_from_stored_document(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            blob_data = blob.download_blob().readall()

        document_analysis_client = DocumentAnalysisClient(config['form_recognizer_endpoint'], AzureKeyCredential(config['form_recognizer_key']))
        poller = document_analysis_client.begin_analyze_document('prebuilt-document', blob_data)
        result = poller.result()

        extracted_text = ''
        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + ' '
    return {'extracted_text': extracted_text}