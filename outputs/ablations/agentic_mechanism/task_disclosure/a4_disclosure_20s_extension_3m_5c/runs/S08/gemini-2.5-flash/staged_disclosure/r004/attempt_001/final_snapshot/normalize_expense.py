from google.cloud import documentai_v1 as documentai
import os

def normalize_expense_with_documentai(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> dict:
    """
    Normalizes expense fields from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the expense processor.
        file_path: The path to the document file (e.g., a receipt image or PDF).
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

    Returns:
        A dictionary containing the normalized expense entities.
    """

    # Create a client
    documentai_client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Create a document object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Process the document
    result = documentai_client.process_document(request=request)
    document = result.document

    # Extract and normalize entities
    normalized_expenses = {}
    for entity in document.entities:
        if entity.type_ and entity.mention_text:
            normalized_expenses[entity.type_] = entity.mention_text

    return normalized_expenses

if __name__ == "__main__":
    # Example Usage: Replace with your actual project_id, location, processor_id, and file details
    # Make sure to install the Google Cloud Document AI client library:
    # pip install google-cloud-documentai

    # Set up Google Cloud authentication (e.g., via GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # For more information, see: https://cloud.google.com/docs/authentication/production

    # Example environment variables (replace with your actual values)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    location = "us"  # Replace with your processor's location (e.g., "us", "eu")
    processor_id = "your-processor-id"  # Replace with your Document AI expense processor ID
    
    # Path to your expense document (e.g., a receipt image or PDF)
    # For demonstration, you might need a dummy file.
    # file_to_process = "path/to/your/receipt.pdf"
    # file_mime_type = "application/pdf"

    # print(f"Normalizing expense from: {file_to_process}")
    # try:
    #     normalized_data = normalize_expense_with_documentai(
    #         project_id, location, processor_id, file_to_process, file_mime_type
    #     )
    #     print("Normalized Expense Data:")
    #     for key, value in normalized_data.items():
    #         print(f"  {key}: {value}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
