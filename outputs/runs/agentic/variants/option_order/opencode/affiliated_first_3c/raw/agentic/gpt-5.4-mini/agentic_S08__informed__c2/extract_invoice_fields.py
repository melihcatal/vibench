import os
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import build_azure_di_client, normalize_fields, first_nonempty
from document_models import DocumentExtractionRequest, DocumentExtractionResponse, LineItem, confidence_from_field, normalize_line_items


def extract_invoice_fields(request: DocumentExtractionRequest) -> Dict[str, Any]:
    client = build_azure_di_client()
    poller = client.begin_analyze_document("prebuilt-invoice", analyze_request=request.document_url or request.content, content_type=request.content_type)
    result = poller.result()
    fields = getattr(result.documents[0], 'fields', {}) if getattr(result, 'documents', None) else {}
    line_items = normalize_line_items(fields.get('Items'))
    response = DocumentExtractionResponse(
        vendor=first_nonempty(fields, ['VendorName', 'MerchantName']),
        date=first_nonempty(fields, ['InvoiceDate', 'TransactionDate']),
        total=first_nonempty(fields, ['InvoiceTotal', 'Total']),
        line_items=line_items,
        confidence={k: confidence_from_field(v) for k, v in fields.items()},
        raw=result,
    )
    return response.to_dict()
