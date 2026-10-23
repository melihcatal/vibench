from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_document_service_config


def extract_fields_from_text(text: str) -> dict:
    cfg = load_document_service_config()
    client = DocumentIntelligenceClient(cfg.endpoint, AzureKeyCredential(cfg.key))
    poller = client.begin_analyze_document("prebuilt-invoice", text)
    result = poller.result()
    fields = {}
    for name, field in result.documents[0].fields.items():
        fields[name] = field.value if hasattr(field, "value") else field.content
    return fields
