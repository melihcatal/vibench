from document_client import DocumentClient
from document_models import DocumentExtractionRequest, InvoiceExtraction


def extract_invoice_fields(
    file_path: str = None,
    file_bytes: bytes = None,
    content_type: str = "application/pdf",
) -> InvoiceExtraction:
    client = DocumentClient()
    request = DocumentExtractionRequest(
        file_path=file_path,
        file_bytes=file_bytes,
        content_type=content_type,
    )
    result = client.parse_invoice(request)
    return result


def extract_invoice_fields_batch(file_paths: list[str]) -> list[InvoiceExtraction]:
    results = []
    for fp in file_paths:
        result = extract_invoice_fields(file_path=fp)
        results.append(result)
    return results


def get_invoice_summary_fields(result: InvoiceExtraction) -> dict:
    return {
        "vendor_name": result.vendor_name.value,
        "vendor_confidence": result.vendor_name.confidence,
        "invoice_date": result.invoice_date.value,
        "date_confidence": result.invoice_date.confidence,
        "invoice_total": result.invoice_total.value,
        "total_confidence": result.invoice_total.confidence,
        "line_item_count": len(result.line_items),
    }
