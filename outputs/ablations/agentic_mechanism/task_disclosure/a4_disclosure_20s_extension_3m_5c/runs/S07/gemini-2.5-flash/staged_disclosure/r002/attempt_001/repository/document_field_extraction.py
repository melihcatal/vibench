from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_fields_from_document_text(
    project_id: str,
    location: str,
    processor_id: str,
    document_text: str,
) -> documentai.Document:
    """
    Extracts structured fields from OCR-normalized document text using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the Document AI processor to use.
        document_text: The OCR-normalized document text to process.

    Returns:
        A Document object containing the extracted entities.
    """

    # You can set client_options to change the endpoint if needed
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Create the document
    document = documentai.Document(content=document_text, mime_type="text/plain")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, document=document)

    result = client.process_document(request=request)
    return result.document

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Replace with your actual project ID, location, and processor ID.
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "your-processor-id"  # e.g., a FORM_PARSER_PROCESSOR_ID

    sample_document_text = """
    Invoice Number: INV-2023-001
    Date: 2023-10-26
    Total Amount: $123.45
    Vendor: Example Corp
    """

    print("Extracting fields using Google Cloud Document AI...")
    try:
        document_result = extract_fields_from_document_text(
            PROJECT_ID, LOCATION, PROCESSOR_ID, sample_document_text
        )

        print("Document processing complete.")
        print("Entities extracted:")
        for entity in document_result.entities:
            print(f"  {entity.type_}: {entity.mention_text} (confidence: {entity.confidence:.2f})")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated to Google Cloud and provided valid project, location, and processor IDs.")
        print("Also, make sure the Document AI API is enabled in your Google Cloud project.")
