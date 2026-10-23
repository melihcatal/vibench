from __future__ import annotations

from document_client import AzureDocumentExtractionClient, extraction_result_to_dict


PROVIDER = "Azure Document Intelligence"
MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(document_bytes: bytes) -> dict:
    client = AzureDocumentExtractionClient()
    result = client.analyze_invoice(document_bytes)
    payload = extraction_result_to_dict(result)
    return {
        "provider": PROVIDER,
        "model_id": MODEL_ID,
        "extracted_fields": {
            "vendor": payload.get("vendor"),
            "date": payload.get("date"),
            "total": payload.get("total"),
            "line_items": payload.get("line_items", []),
        },
        "raw_response": payload.get("raw_response", {}),
    }
