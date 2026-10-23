from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_service_config


def validate_document_fields(document_bytes: bytes) -> dict:
    config = load_service_config("AZURE_DOCUMENT_INTELLIGENCE")
    client = DocumentIntelligenceClient(
        config.endpoint, AzureKeyCredential(config.api_key)
    )
    poller = client.begin_analyze_document("prebuilt-document", document=document_bytes)
    result = poller.result()
    doc = result.documents[0] if result.documents else None
    fields = doc.fields if doc else {}
    required = ["vendor", "date", "total"]
    scores = {
        name: getattr(fields.get(name.capitalize()), "confidence", 0.0)
        for name in required
    }
    return {"valid": all(scores.values()), "confidence_scores": scores}
