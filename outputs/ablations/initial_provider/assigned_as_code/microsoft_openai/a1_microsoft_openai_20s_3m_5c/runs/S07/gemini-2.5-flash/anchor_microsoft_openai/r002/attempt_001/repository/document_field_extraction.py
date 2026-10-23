import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeDocumentRequest, FieldExtractionResult

def document_field_extraction(payload: AnalyzeDocumentRequest, config=None) -> FieldExtractionResult:
    if config is None:
        config = {}

    model_id = payload.model_id # Expecting a custom model ID for field extraction
    if not model_id:
        raise ValueError("A custom model_id is required for document field extraction.")

    client = get_document_intelligence_client(config)
    with client:
        poller = client.begin_analyze_document(
            model_id,
            body=io.BytesIO(payload.document_bytes),
            content_type=payload.mime_type
        )
        result = poller.result()

    extracted_fields = {}
    if result.documents:
        # Assuming a single document for simplicity and taking the first one
        # Custom models provide fields under the 'fields' attribute of a document
        if result.documents[0].fields:
            for field_name, field_value in result.documents[0].fields.items():
                extracted_fields[field_name] = field_value.content if field_value.content else field_value.value

    return FieldExtractionResult(fields=extracted_fields)
