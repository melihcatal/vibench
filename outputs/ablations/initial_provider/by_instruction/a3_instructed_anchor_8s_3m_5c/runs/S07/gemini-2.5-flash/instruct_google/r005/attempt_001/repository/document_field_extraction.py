from google.cloud import documentai_v1 as documentai
from typing import Dict, Any
from document_models import DocumentInput, ExtractedText

def extract_structured_fields(document_input: DocumentInput, project_id: str, location: str, processor_id: str) -> Dict[str, Any]:
    """Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.

    This function assumes a Document AI processor (e.g., a custom extractor or a specialized pre-trained processor)
    is used to extract structured fields.
    """
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # For text-based processing, we can pass the text directly or a document with text content.
    # Assuming the input is an image, we'll process it to get the structured fields.
    # If the input was already OCR-normalized text, the approach would be slightly different.
    with open(document_input.image_path, "rb") as image_file:
        image_content = image_file.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_fields = {}
    for entity in document.entities:
        # Entities represent structured fields extracted by the processor.
        # The exact structure depends on the processor configuration.
        # This is a generic way to extract information.
        if entity.type_:
            field_value = documentai.Document.to_markdown(entity.text_anchor, document.text)
            extracted_fields[entity.type_] = field_value.strip()
            # You might need to handle properties or other nested entities for more complex structures
            if entity.properties:
                for prop in entity.properties:
                    prop_value = documentai.Document.to_markdown(prop.text_anchor, document.text)
                    extracted_fields[f"{entity.type_}.{prop.type_}"] = prop_value.strip()

    return extracted_fields

if __name__ == "__main__":
    # Example usage: Replace with your project_id, location, processor_id and a valid image path
    # PROJECT_ID = "your-gcp-project-id"
    # LOCATION = "us"
    # PROCESSOR_ID = "your-document-ai-custom-extractor-processor-id"
    # document_input = DocumentInput(image_path="path/to/your/document_for_fields.png", mime_type="image/png")
    # structured_fields = extract_structured_fields(document_input, PROJECT_ID, LOCATION, PROCESSOR_ID)
    # print(structured_fields)
    pass
