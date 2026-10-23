from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os
from typing import List, Dict, Any

def extract_structured_fields(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> List[Dict[str, Any]]:
    """Extracts structured fields from a document using a specific Document AI processor (e.g., Invoice Parser)."""

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The processor_id here should correspond to a specialized processor, e.g., "invoice-parser"
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = []

    for entity in document.entities:
        # Entities from specialized processors like Invoice Parser have specific types
        # and usually a `mentionText` or `normalizedValue`.
        field_name = entity.type_
        field_value = entity.mention_text if entity.mention_text else ""
        confidence = entity.confidence
        detected_text = entity.text_anchor.text_content if entity.text_anchor.text_segments else ""
        
        # For normalized values, check entity.normalized_value
        # e.g., if entity.type_ == "invoice_date" and entity.normalized_value.date_value:
        #    field_value = str(entity.normalized_value.date_value)

        extracted_fields.append({
            "field_name": field_name,
            "field_value": field_value,
            "confidence": confidence,
            "detected_text": detected_text,
        })
    
    return extracted_fields

if __name__ == '__main__':
    # Placeholder for actual usage, replace with your project details and a dummy file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # Use a specialized processor like "invoice-parser" or "receipt-parser"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us" # e.g., "us"
    processor_id = os.getenv("DOCUMENTAI_FIELD_EXTRACTION_PROCESSOR_ID", "your-invoice-parser-id") # e.g., "invoice-parser"
    
    # Create a dummy image file for testing
    dummy_file_path = "dummy.pdf"
    with open(dummy_file_path, "wb") as f:
        f.write(b"dummy pdf content") # Replace with actual PDF content for real testing

    try:
        # result_fields = extract_structured_fields(project_id, location, processor_id, dummy_file_path, "application/pdf")
        # print(f"Extracted Fields: {result_fields}")
        print("Run with actual Document AI credentials and a valid specialized processor ID and PDF file.")
    except Exception as e:
        print(f"Error extracting structured fields: {e}")
    finally:
        os.remove(dummy_file_path)
