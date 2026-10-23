import os
from typing import Any, Dict

from google.cloud import documentai

from document_client import build_processor_path, get_document_ai_client
from document_models import DocumentResponse, parse_document_ai_response


def extract_invoice_fields(
    gcs_uri: str, location: str = "us", processor_id: str = None
) -> Dict[str, Any]:
    client = get_document_ai_client()
    processor_id = processor_id or os.environ.get(
        "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID", ""
    )
    name = build_processor_path(location, processor_id)
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(uri=gcs_uri, mime_type="application/pdf"),
    )
    result = client.process_document(request=request)
    parsed: DocumentResponse = parse_document_ai_response(result.document, "invoice")
    return {
        "document_type": parsed.document_type,
        "fields": {
            f.name: {"value": f.value, "confidence": f.confidence}
            for f in parsed.fields
        },
        "raw": parsed.raw,
    }
