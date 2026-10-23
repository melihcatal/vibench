import json
from typing import Any, Dict, Optional

from document_client import StructuredDocumentClient, load_document_settings
from document_models import DocumentExtractionRequest, ExtractionResult, coerce_text_payload


def extract_invoice_fields(document: Any, model: Optional[str] = None) -> Dict[str, Any]:
    settings = load_document_settings()
    client = StructuredDocumentClient(settings)
    prompt = "Extract vendor, date, total, currency, and line items from this invoice. Return structured JSON with confidence per field."
    request = DocumentExtractionRequest(
        document_text=coerce_text_payload(document),
        task_name="invoice_extraction",
        instructions=prompt,
        model=model or settings.openai_model,
        schema_name="invoice_fields",
    )
    result: ExtractionResult = client.extract(request)
    return result.to_dict()


def main() -> None:
    import sys

    payload = sys.stdin.read()
    print(json.dumps(extract_invoice_fields(payload), ensure_ascii=False))
