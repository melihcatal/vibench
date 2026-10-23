import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

AZURE_DI_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_DI_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

PREBUILT_INVOICE_MODEL_ID = "prebuilt-invoice"
PREBUILT_RECEIPT_MODEL_ID = "prebuilt-receipt"


def get_document_intelligence_client():
    if not AZURE_DI_ENDPOINT or not AZURE_DI_KEY:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY "
            "must be set for Azure Document Intelligence"
        )
    credential = AzureKeyCredential(AZURE_DI_KEY)
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DI_ENDPOINT,
        credential=credential,
    )
    return client


def analyze_document_from_file(
    client, model_id, file_path, content_type="application/pdf"
):
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=model_id,
            analyze_request=f,
            content_type=content_type,
        )
        result = poller.result()
    return result


def analyze_document_from_bytes(
    client, model_id, file_bytes, content_type="application/pdf"
):
    from io import BytesIO

    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=BytesIO(file_bytes),
        content_type=content_type,
    )
    result = poller.result()
    return result


def extract_field_value(field, default=None):
    if field is None:
        return default
    if hasattr(field, "value"):
        return field.value
    return default


def extract_field_confidence(field, default=0.0):
    if field is None:
        return default
    if hasattr(field, "confidence"):
        return field.confidence
    return default
