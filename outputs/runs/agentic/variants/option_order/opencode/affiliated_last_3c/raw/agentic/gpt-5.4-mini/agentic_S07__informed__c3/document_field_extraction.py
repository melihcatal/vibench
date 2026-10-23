from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_config
from document_models import DocumentRequest, normalize_key_values, normalize_text


def document_field_extraction(request: DocumentRequest) -> dict:
    cfg = get_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(cfg["endpoint"], AzureKeyCredential(cfg["key"]))
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        analyze_request=request.content,
        content_type=request.mime_type,
    )
    result = poller.result()
    fields = {}
    for name, field in (
        getattr(result, "documents", [])[0].fields.items()
        if getattr(result, "documents", None)
        else []
    ):
        fields[normalize_text(name)] = normalize_text(
            getattr(field, "content", None) or getattr(field, "value", None)
        )
    if not fields:
        fields = normalize_key_values(getattr(result, "key_value_pairs", []) or [])
    return fields
