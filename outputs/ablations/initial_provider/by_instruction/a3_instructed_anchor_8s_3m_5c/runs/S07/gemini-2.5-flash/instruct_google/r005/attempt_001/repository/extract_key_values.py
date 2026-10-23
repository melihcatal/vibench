from google.cloud import documentai_v1 as documentai
from typing import Dict, Any
from document_models import DocumentInput, ExtractedKeyValuePairs

def extract_key_values_from_document(document_input: DocumentInput, project_id: str, location: str, processor_id: str) -> ExtractedKeyValuePairs:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI.

    This function assumes a Document AI Form Parser processor is used.
    """
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    with open(document_input.image_path, "rb") as image_file:
        image_content = image_file.read()

    # Configure the process request
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_kv_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = documentai.Document.to_markdown(form_field.field_name.text_anchor, document.text)
            field_value = documentai.Document.to_markdown(form_field.field_value.text_anchor, document.text)
            extracted_kv_pairs[field_name.strip()] = field_value.strip()
            
    return ExtractedKeyValuePairs(key_value_pairs=extracted_kv_pairs)

if __name__ == "__main__":
    # Example usage: Replace with your project_id, location, processor_id and a valid image path
    # PROJECT_ID = "your-gcp-project-id"
    # LOCATION = "us"
    # PROCESSOR_ID = "your-document-ai-form-parser-processor-id"
    # document_input = DocumentInput(image_path="path/to/your/form_document.png", mime_type="image/png")
    # extracted_kv = extract_key_values_from_document(document_input, PROJECT_ID, LOCATION, PROCESSOR_ID)
    # print(extracted_kv.key_value_pairs)
    pass
