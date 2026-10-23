from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_service_config


def extract_text(document_url: str) -> str:
    cfg = load_document_service_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document("prebuilt-read", document_url)
    result = poller.result()
    return "\n".join(line.content for page in result.pages for line in page.lines)
