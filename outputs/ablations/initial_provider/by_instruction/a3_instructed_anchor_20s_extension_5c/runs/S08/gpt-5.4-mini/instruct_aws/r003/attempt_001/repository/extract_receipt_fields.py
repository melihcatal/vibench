from typing import Any, Dict

from document_client import parse_textract_response, textract_client


def extract_receipt_fields(document_bytes: bytes = None) -> Dict[str, Any]:
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": document_bytes},
        FeatureTypes=["FORMS", "TABLES"],
    )
    parsed = parse_textract_response(response)
    return {
        "merchant": parsed.fields.get("merchant", parsed.fields.get("vendor")),
        "tax": parsed.fields.get("tax"),
        "total": parsed.fields.get("total"),
        "items": parsed.fields.get("items", []),
        "provider": parsed.provider,
    }
