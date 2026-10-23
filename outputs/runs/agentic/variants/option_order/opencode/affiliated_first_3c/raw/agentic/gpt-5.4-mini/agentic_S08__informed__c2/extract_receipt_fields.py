from typing import Any, Dict

from document_client import build_azure_di_client, first_nonempty
from document_models import DocumentExtractionRequest, DocumentExtractionResponse, confidence_from_field, normalize_line_items


def extract_receipt_fields(request: DocumentExtractionRequest) -> Dict[str, Any]:
    client = build_azure_di_client()
    poller = client.begin_analyze_document("prebuilt-receipt", analyze_request=request.document_url or request.content, content_type=request.content_type)
    result = poller.result()
    fields = getattr(result.documents[0], 'fields', {}) if getattr(result, 'documents', None) else {}
    response = DocumentExtractionResponse(
        vendor=first_nonempty(fields, ['MerchantName', 'VendorName']),
        tax=first_nonempty(fields, ['TotalTax', 'Tax']),
        total=first_nonempty(fields, ['Total', 'ReceiptTotal']),
        items=normalize_line_items(fields.get('Items')),
        confidence={k: confidence_from_field(v) for k, v in fields.items()},
        raw=result,
    )
    return response.to_dict()
