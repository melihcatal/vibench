from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_service_config
from document_models import normalize_blocks


def extract_layout(document_url: str):
    cfg = load_document_service_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document("prebuilt-layout", document_url)
    result = poller.result()
    raw = result.to_dict()
    return normalize_blocks({"blocks": raw.get("paragraphs", [])})
