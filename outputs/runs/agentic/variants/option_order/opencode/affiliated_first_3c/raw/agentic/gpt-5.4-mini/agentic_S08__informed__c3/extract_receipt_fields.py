from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import build_azure_client, read_bytes
from document_models import (
    DocumentExtractionRequest,
    DocumentExtractionResponse,
    as_line_items,
    normalize_confidence,
)


def extract_receipt_fields(
    request: DocumentExtractionRequest,
) -> DocumentExtractionResponse:
    client = build_azure_client()
    poller = client.begin_analyze_document(
        "prebuilt-receipt", AnalyzeDocumentRequest(bytes_source=read_bytes(request))
    )
    result = poller.result()
    fields = result.documents[0].fields if getattr(result, "documents", None) else {}
    return DocumentExtractionResponse(
        provider="azure-document-intelligence-prebuilt-receipt",
        fields={
            "merchant": getattr(fields.get("MerchantName"), "value", None)
            if fields
            else None,
            "tax": getattr(fields.get("TotalTax"), "value", None) if fields else None,
            "total": getattr(fields.get("Total"), "value", None) if fields else None,
            "items": as_line_items(
                getattr(
                    fields.get("Items").value
                    if fields and fields.get("Items")
                    else None,
                    "value",
                    None,
                )
                if False
                else getattr(fields.get("Items"), "value", None)
                if fields
                else None
            ),
            "confidence": normalize_confidence(
                getattr(fields.get("Total"), "confidence", 0.0) if fields else 0.0
            ),
        },
        raw=result,
    )
