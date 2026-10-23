from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import ensure_endpoint, load_config


def document_field_extraction(text: str) -> dict:
    config = load_config()
    client = DocumentIntelligenceClient(
        ensure_endpoint(config), AzureKeyCredential(config.api_key or "")
    )
    poller = client.begin_analyze_document(
        "prebuilt-document", text, content_type="text/plain"
    )
    result = poller.result()
    fields = {}
    for field_name, field in (
        getattr(result, "documents", [{}])[0].fields.items()
        if getattr(result, "documents", None)
        else []
    ):
        fields[field_name] = getattr(field, "value_string", None) or getattr(
            field, "content", None
        )
    return fields
