import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

AZURE_DI_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://default.cognitiveservices.azure.com/",
)
AZURE_DI_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

PREBUILT_INVOICE_MODEL_ID = "prebuilt-invoice"
PREBUILT_RECEIPT_MODEL_ID = "prebuilt-receipt"


def get_document_client():
    credential = AzureKeyCredential(AZURE_DI_KEY)
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DI_ENDPOINT, credential=credential
    )
    return client


def analyze_document_bytes(
    client, document_bytes, model_id, content_type="application/pdf"
):
    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=AnalyzeDocumentRequest(bytes_source=document_bytes),
        content_type=content_type,
    )
    result = poller.result()
    return result


def analyze_document_url(client, document_url, model_id):
    poller = client.begin_analyze_document(
        model_id=model_id,
        analyze_request=AnalyzeDocumentRequest(url_source=document_url),
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


def extract_line_items_from_table(table):
    items = []
    if not table or not table.cells:
        return items
    row_data = {}
    for cell in table.cells:
        row_idx = cell.row_index
        col_idx = cell.column_index
        if row_idx not in row_data:
            row_data[row_idx] = {}
        row_data[row_idx][col_idx] = cell.content
    for row_idx in sorted(row_data.keys()):
        items.append(row_data[row_idx])
    return items
