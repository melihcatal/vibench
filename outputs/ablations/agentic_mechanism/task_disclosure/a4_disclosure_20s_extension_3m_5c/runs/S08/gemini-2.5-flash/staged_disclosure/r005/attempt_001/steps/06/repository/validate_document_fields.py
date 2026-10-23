
import os
from google.cloud import documentai_v1 as documentai

def validate_document_fields(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str,
                             required_fields_with_min_confidence: dict) -> dict:
    """
    Validates required structured fields and their confidence scores in a document
    using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the Document AI processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").
        required_fields_with_min_confidence: A dictionary where keys are field names
                                             and values are the minimum required confidence scores (0.0-1.0).

    Returns:
        A dictionary containing validation results.
    """
    documentai_client = documentai.DocumentProcessorServiceClient()
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    response = documentai_client.process_document(request=request)
    document = response.document

    validation_results = {"overall_valid": True, "field_validations": {}}

    for field_name, min_confidence in required_fields_with_min_confidence.items():
        found_field = False
        field_confidence = 0.0
        for entity in document.entities:
            if entity.type_ == field_name:
                found_field = True
                if entity.confidence:
                    field_confidence = entity.confidence
                break
        
        is_valid = found_field and field_confidence >= min_confidence
        validation_results["field_validations"][field_name] = {
            "found": found_field,
            "confidence": field_confidence,
            "min_required_confidence": min_confidence,
            "is_valid": is_valid
        }
        if not is_valid:
            validation_results["overall_valid"] = False

    return validation_results

