from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_client


def stored_document_ocr(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload['object_name'])
    content = blob.download_blob().readall()
    client = DocumentAnalysisClient(config['form_recognizer_endpoint'], AzureKeyCredential(config['form_recognizer_key']))
    poller = client.begin_analyze_document('prebuilt-read', content)
    result = poller.result()
    return {'object_name': payload['object_name'], 'text': '\n'.join(line.content for page in result.pages for line in page.lines)}
