from document_client import DocumentClient
from document_models import DocumentExtractionRequest, ReceiptExtraction


def extract_receipt_fields(
    file_path: str = None,
    file_bytes: bytes = None,
    content_type: str = "application/pdf",
) -> ReceiptExtraction:
    client = DocumentClient()
    request = DocumentExtractionRequest(
        file_path=file_path,
        file_bytes=file_bytes,
        content_type=content_type,
    )
    result = client.parse_receipt(request)
    return result


def extract_receipt_fields_batch(file_paths: list[str]) -> list[ReceiptExtraction]:
    results = []
    for fp in file_paths:
        result = extract_receipt_fields(file_path=fp)
        results.append(result)
    return results


def get_receipt_summary_fields(result: ReceiptExtraction) -> dict:
    return {
        "merchant_name": result.merchant_name.value,
        "merchant_confidence": result.merchant_name.confidence,
        "tax_amount": result.tax_amount.value,
        "tax_confidence": result.tax_amount.confidence,
        "receipt_total": result.receipt_total.value,
        "total_confidence": result.receipt_total.confidence,
        "item_count": len(result.items),
    }
