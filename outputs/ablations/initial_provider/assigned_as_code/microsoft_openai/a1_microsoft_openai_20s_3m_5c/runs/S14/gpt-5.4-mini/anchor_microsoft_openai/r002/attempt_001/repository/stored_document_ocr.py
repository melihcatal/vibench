from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_blob_service_client


def stored_document_ocr(payload, config=None):
    config = config or {}
    with get_blob_service_client(config) as storage_client:
        blob = storage_client.get_blob_client(container=config['container'], blob=payload['object_name'])
        data = blob.download_blob().readall()
    client = DocumentAnalysisClient(config['form_recognizer_endpoint'], AzureKeyCredential(config['form_recognizer_key']))
    poller = client.begin_analyze_document('prebuilt-read', document=data)
    result = poller.result()
    lines = []
    for page in result.pages:
        for line in page.lines:
            lines.append(line.content)
    return {'text': '\n'.join(lines), 'pages': len(result.pages)}
