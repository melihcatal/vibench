import json
from typing import Any, Dict, Optional

from document_client import StructuredDocumentClient, load_document_settings
from document_models import DocumentExtractionRequest, ExtractionResult, coerce_text_payload


def extract_receipt_fields(document: Any, model: Optional[str] = None) -> Dict[str, Any]:
    settings = load_document_settings()
    client = StructuredDocumentClient(settings)
    prompt = "Extract merchant, tax, total, currency, date, and items from this receipt. Return structured JSON with confidence per field.")
    request = DocumentExtractionRequest(
        document_text=coerce_text_payload(document),
        task_name="receipt_extraction",
        instructions=prompt,
        model=model or settings.openai_model,
        schema_name="receipt_fields",
    )
    result: ExtractionResult = client.extract(request)
    return result.to_dict()


def main() -> None:
    import sys

    payload = sys.stdin.read()
    print(json.dumps(extract_receipt_fields(payload), ensure_ascii=False))
