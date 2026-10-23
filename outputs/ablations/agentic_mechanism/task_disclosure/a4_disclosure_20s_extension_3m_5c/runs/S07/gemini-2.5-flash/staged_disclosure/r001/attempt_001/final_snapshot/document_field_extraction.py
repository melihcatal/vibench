import os
from google.cloud import documentai_v1 as documentai

def extract_fields_from_document(project_id: str, location: str, processor_id: str, document_text: str):
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.
    """
    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # You can also use a GCS URI for a real document
    document = documentai.types.Document(text=document_text)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        document=document,
    )

    result = client.process_document(request=request)

    # For demonstration, we'll just print detected entities
    # In a real application, you would parse result.document.entities
    # and result.document.pages.form_fields to extract the structured data.
    
    print("Document processing complete.")
    if result.document.entities:
        print("Detected Entities:")
        for entity in result.document.entities:
            print(f"  Type: {entity.type_}, Mention Text: {entity.mention_text}")
    
    if result.document.text_changes:
        print("Text Changes (OCR normalization):")
        for text_change in result.document.text_changes:
            print(f"  {text_change.original_text} -> {text_change.changed_text}")

    return result.document

if __name__ == "__main__":
    # Replace with your actual project ID, location, and processor ID
    # A processor needs to be created in Google Cloud Document AI for form parsing or custom entity extraction.
    # Example: project_id = "your-gcp-project-id"
    # Example: location = "us" # e.g., "us" or "eu"
    # Example: processor_id = "your-processor-id" # e.g., "YOUR_PROCESSOR_ID" for a Form Parser or Custom Extractor

    # Placeholder for credentials. In a real application, authenticate using
    # Google Cloud credentials (e.g., service account or gcloud default credentials).
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    sample_document_text = """
    Invoice # 12345
    Date: 2026-09-20
    Amount Due: $150.75
    Item: Laptop
    Quantity: 1
    Price: $120.00
    Tax: $30.75
    Total: $150.75
    """

    # Example usage (uncomment and fill in details to run):
    # try:
    #     processed_document = extract_fields_from_document(
    #         project_id="your-gcp-project-id",
    #         location="us",
    #         processor_id="your-processor-id",
    #         document_text=sample_document_text
    #     )
    #     # Further processing of the document object
    # except Exception as e:
    #     print(f"An error occurred: {e}")
