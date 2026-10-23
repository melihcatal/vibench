
from google.cloud import documentai_v1beta3 as documentai

def validate_document_fields(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    required_fields: dict,
    min_confidence: float = 0.9
):
    """
    Validates required structured fields and their confidence scores in a document
    using Google Cloud Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud location (e.g., "us").
        processor_id (str): The ID of the Document AI processor to use.
        file_path (str): The path to the document file.
        mime_type (str): The MIME type of the document (e.g., "application/pdf").
        required_fields (dict): A dictionary where keys are field names and values
                                are the expected types (e.g., {"invoice_id": str, "total_amount": float}).
        min_confidence (float): The minimum confidence score required for a field.

    Returns:
        dict: A dictionary containing validation results.
    """
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    validation_results = {
        "overall_status": "success",
        "field_validations": {}
    }

    for field_name, expected_type in required_fields.items():
        field_found = False
        field_confident = False
        field_value = None

        for entity in document.entities:
            if entity.type_ == field_name:
                field_found = True
                field_value = entity.text_anchor.content if entity.text_anchor else entity.mention_text
                if entity.confidence >= min_confidence:
                    field_confident = True
                break

        validation_results["field_validations"][field_name] = {
            "found": field_found,
            "confident": field_confident,
            "value": field_value,
            "expected_type": str(expected_type),
            "actual_type_match": False
        }

        if not field_found or not field_confident:
            validation_results["overall_status"] = "failed"
        else:
            try:
                if expected_type == str:
                    validation_results["field_validations"][field_name]["actual_type_match"] = isinstance(field_value, str)
                elif expected_type == int:
                    validation_results["field_validations"][field_name]["actual_type_match"] = isinstance(int(field_value), int)
                elif expected_type == float:
                    validation_results["field_validations"][field_name]["actual_type_match"] = isinstance(float(field_value), float)
                # Add more type checks as needed
                if not validation_results["field_validations"][field_name]["actual_type_match"]:
                     validation_results["overall_status"] = "failed"
            except (ValueError, TypeError):
                validation_results["overall_validations"] = "failed"

    return validation_results
