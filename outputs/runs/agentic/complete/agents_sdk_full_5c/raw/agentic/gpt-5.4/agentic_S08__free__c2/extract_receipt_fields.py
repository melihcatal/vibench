from __future__ import annotations

from document_client import AzureDocumentExtractionClient, extraction_result_to_dict


PROVIDER = "Azure Document Intelligence"
MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(document_bytes: bytes) -> dict:
    client = AzureDocumentExtractionClient()
    result = client.analyze_receipt(document_bytes)
    payload = extraction_result_to_dict(result)
    return {
        "provider": PROVIDER,
        "model_id": MODEL_ID,
        "extracted_fields": {
            "merchant": payload.get("merchant"),
            "tax": payload.get("tax"),
            "total": payload.get("total"),
            "items": payload.get("line_items", []),
        },
        "raw_response": payload.get("raw_response", {}),
    }
