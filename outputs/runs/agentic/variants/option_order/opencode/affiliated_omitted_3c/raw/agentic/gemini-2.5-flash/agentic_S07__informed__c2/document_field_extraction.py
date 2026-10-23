from document_client import get_document_client
from document_models import AnalyzeResult


def document_field_extraction(document_stream: bytes) -> dict:
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-invoice", document_stream, content_type="application/octet-stream"
    )
    result = poller.result()

    extracted_fields = {}
    if result.documents:
        for doc in result.documents:
            if doc.fields:
                for field_name, field_value in doc.fields.items():
                    extracted_fields[field_name] = {
                        "value": field_value.content,
                        "confidence": field_value.confidence,
                        "kind": str(field_value.kind),
                    }
    return extracted_fields
