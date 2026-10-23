import os
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values(image_content: bytes, project_id: str, location: str, processor_id: str) -> documentai.Document:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI (Form Parser)."""
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF for forms

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    response = client.process_document(request=request)

    # The response.document object contains the extracted entities (key-value pairs) within its entities field.
    return response.document

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _location = "us"
    _processor_id = os.environ.get("DOCUMENT_AI_FORM_PARSER_ID", "your-form-parser-processor-id") # Replace with your form parser ID

    _dummy_pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 11>>stream\nBT /F1 12 Tf ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000109 00000 n\n0000000216 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n277\n%%EOF"
    print(f"Using Document AI Form Parser Processor: {_processor_id}")
    # _document = extract_key_values(_dummy_pdf_content, _project_id, _location, _processor_id)
    # if _document and _document.entities:
    #     for entity in _document.entities:
    #         if entity.type_ == "form_field" and entity.properties:
    #             key = _document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index]
    #             value = _document.text[entity.properties[0].text_anchor.text_segments[0].start_index:entity.properties[0].text_anchor.text_segments[0].end_index]
    #             print(f"Key: {key}, Value: {value}")
    print("Key-value extraction example is commented out. Provide a real PDF and credentials to run.")
