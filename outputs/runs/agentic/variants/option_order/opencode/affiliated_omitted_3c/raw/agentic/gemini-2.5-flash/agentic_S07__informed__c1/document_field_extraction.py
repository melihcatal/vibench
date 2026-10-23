from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_document_intelligence_client
from document_models import DocumentInput, FieldExtractionResult


def extract_document_fields(doc_input: DocumentInput) -> FieldExtractionResult:
    client = get_document_intelligence_client()

    # Use the prebuilt-invoice model for structured field extraction as an example
    # For other document types, a different prebuilt model or a custom model would be used.
    model_id = "prebuilt-invoice"

    if doc_input.document_url:
        poller = client.begin_analyze_document(
            model_id, document_url=doc_input.document_url
        )
    elif doc_input.document_bytes and doc_input.content_type:
        poller = client.begin_analyze_document(
            model_id,
            analyze_request=doc_input.document_bytes,
            content_type=doc_input.content_type,
        )
    else:
        raise ValueError(
            "Either document_url or document_bytes with content_type must be provided."
        )

    result: AnalyzeResult = poller.result()

    extracted_fields = {}
    if result.documents:
        for doc in result.documents:
            if doc.fields:
                for field_name, field_value in doc.fields.items():
                    extracted_fields[field_name] = {
                        "value": field_value.content,
                        "confidence": field_value.confidence,
                        "bounding_regions": [
                            br.to_dict() for br in field_value.bounding_regions
                        ]
                        if field_value.bounding_regions
                        else [],
                    }

    return FieldExtractionResult(fields=extracted_fields)
