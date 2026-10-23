
import os
from google.cloud import documentai_v1 as documentai

def extract_fields_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    document_text: str,
):
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Create document from text
    document = documentai.Document(text=document_text)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, document=document)

    # Use the Document AI client to process the document
    result = client.process_document(request=request)

    # For a more detailed example of how to parse the result,
    # refer to Google Cloud Document AI documentation for your specific processor type.
    # This example simply prints the entities found.
    print(f"Document processing complete. Found {len(result.document.entities)} entities:")

    for entity in result.document.entities:
        print(f"  Entity type: {entity.type_}, Mention text: {entity.mention_text}")
        if entity.normalized_value:
            print(f"  Normalized value: {entity.normalized_value.text}")
    
    return result.document

if __name__ == "__main__":
    # Replace with your Google Cloud project details
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # e.g., "YOUR_PROCESSOR_ID"

    if not PROJECT_ID or PROCESSOR_ID == "YOUR_PROCESSOR_ID":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable and replace 'YOUR_PROCESSOR_ID' with your actual Document AI processor ID.")
    else:
        # Example OCR-normalized document text
        example_document_text = """
        Invoice # 12345
        Date: 2026-09-20
        Vendor: Example Corp
        Amount Due: $150.75
        """
        print("Extracting fields...")
        extract_fields_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, example_document_text)
