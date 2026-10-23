from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from storage_models import normalize_config, normalize_payload, object_response


def stored_document_ocr(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    client = DocumentAnalysisClient(endpoint=cfg['form_recognizer_endpoint'], credential=AzureKeyCredential(cfg['form_recognizer_key']))
    poller = client.begin_analyze_document_from_url('prebuilt-read', pl['document_url'])
    result = poller.result()
    text = '\n'.join(line.content for page in result.pages for line in page.lines)
    return object_response(pl['object_name'], text=text, pages=len(result.pages))
