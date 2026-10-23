from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os
from typing import List, Dict, Any

def extract_key_values(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> Dict[str, str]:
    """Extracts key-value pairs from a form-like document using Google Document AI."""

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = {}

    # Iterate through entities to find form fields (key-value pairs)
    for entity in document.entities:
        if entity.type == "form_field": # General form field type
            key = ""
            value = ""
            if entity.text_anchor.text_segments:
                key = entity.text_anchor.text_content
            
            for prop in entity.properties:
                if prop.type == "value" and prop.text_anchor.text_segments:
                    value = prop.text_anchor.text_content
                    break
            
            if key and value:
                key_value_pairs[key.strip()] = value.strip()
        # Also look for entities with specific types that might represent key-value pairs
        # For instance, if using a specific processor like "invoice_processor", you might see types like "invoice_date", "total_amount"
        # This general approach tries to capture common form fields.
        elif entity.type_ != "" and entity.text_anchor.text_segments and not entity.properties: # Basic entity as key with its content as value if no properties
             key_value_pairs[entity.type_] = entity.text_anchor.text_content.strip()

    return key_value_pairs

if __name__ == '__main__':
    # Placeholder for actual usage, replace with your project details and a dummy file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # Use a general form parser processor like "form-parser"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us" # e.g., "us"
    processor_id = os.getenv("DOCUMENTAI_KEY_VALUE_PROCESSOR_ID", "your-key-value-processor-id") # e.g., "form-parser"
    
    # Create a dummy image file for testing
    dummy_file_path = "dummy.png"
    with open(dummy_file_path, "wb") as f:
        f.write(b"dummy image content") # Replace with actual image content for real testing

    try:
        # result_key_values = extract_key_values(project_id, location, processor_id, dummy_file_path, "image/png")
        # print(f"Extracted Key-Value Pairs: {result_key_values}")
        print("Run with actual Document AI credentials and a valid processor ID and image file.")
    except Exception as e:
        print(f"Error extracting key-value pairs: {e}")
    finally:
        os.remove(dummy_file_path)
