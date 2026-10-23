from azure.ai.formrecognizer import DocumentAnalysisClient
from storage_client import load_storage_config


def stored_document_ocr(payload, config=None):
    config = load_storage_config(config)
    client = DocumentAnalysisClient(endpoint=config['document_intelligence_endpoint'], credential=config['document_intelligence_credential'])
    result = client.begin_analyze_document_from_url('prebuilt-read', payload['document_url']).result()
    return {'text': '\n'.join(line.content for page in result.pages for line in page.lines)}
