from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_service_config
from document_models import normalize_key_values


def extract_key_values(document_url: str):
    cfg = load_document_service_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document("prebuilt-document", document_url)
    result = poller.result()
    return normalize_key_values(result.to_dict())
