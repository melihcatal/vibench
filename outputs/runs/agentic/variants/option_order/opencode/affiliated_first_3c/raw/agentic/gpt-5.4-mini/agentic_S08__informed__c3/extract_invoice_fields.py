from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import build_azure_client, read_bytes
from document_models import (
    DocumentExtractionRequest,
    DocumentExtractionResponse,
    as_line_items,
    normalize_confidence,
)


def extract_invoice_fields(
    request: DocumentExtractionRequest,
) -> DocumentExtractionResponse:
    client = build_azure_client()
    poller = client.begin_analyze_document(
        "prebuilt-invoice", AnalyzeDocumentRequest(bytes_source=read_bytes(request))
    )
    result = poller.result()
    fields = result.documents[0].fields if getattr(result, "documents", None) else {}
    return DocumentExtractionResponse(
        provider="azure-document-intelligence-prebuilt-invoice",
        fields={
            "vendor": getattr(fields.get("VendorName"), "value", None)
            if fields
            else None,
            "date": getattr(fields.get("InvoiceDate"), "value", None)
            if fields
            else None,
            "total": getattr(fields.get("InvoiceTotal"), "value", None)
            if fields
            else None,
            "line_items": as_line_items(
                getattr(fields.get("Items"), "value", None) if fields else None
            ),
            "confidence": normalize_confidence(
                getattr(fields.get("InvoiceTotal"), "confidence", 0.0)
                if fields
                else 0.0
            ),
        },
        raw=result,
    )
