import os
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us"
PROCESSOR_ID_FORM = os.environ.get("GCP_DOCUMENTAI_FORM_PROCESSOR_ID") # e.g., "form-parser-v2.1-2023-01-26"

def extract_key_values(image_content: bytes) -> documentai.Document:
    """Extracts key-value pairs from a form-like document using Google Cloud Document AI Form Parser."""
    if not all([PROJECT_ID, PROCESSOR_ID_FORM]):
        raise ValueError("Environment variables GCP_PROJECT_ID, GCP_DOCUMENTAI_FORM_PROCESSOR_ID must be set.")

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID_FORM)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Forms often in PDFs

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == 'main':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and required env vars are set.
    os.environ["GCP_PROJECT_ID"] = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    os.environ["GCP_DOCUMENTAI_FORM_PROCESSOR_ID"] = os.environ.get("GCP_DOCUMENTAI_FORM_PROCESSOR_ID", "form-parser") # Use 'form-parser' for the pre-trained form parser

    try:
        with open("example_form.pdf", "rb") as document_file:
            content = document_file.read()
        document = extract_key_values(content)
        print("Document Entities (Key-Value pairs) found:", len(document.entities))
        for entity in document.entities:
            if entity.type_ == "form_field":
                key = entity.mention_text
                value = entity.normalized_value.text if entity.normalized_value else entity.text_anchor.text_segments[0].text if entity.text_anchor.text_segments else ""
                print(f"Key: {key}, Value: {value}")
    except FileNotFoundError:
        print("Please create an 'example_form.pdf' file or replace the path with a valid document.")
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
