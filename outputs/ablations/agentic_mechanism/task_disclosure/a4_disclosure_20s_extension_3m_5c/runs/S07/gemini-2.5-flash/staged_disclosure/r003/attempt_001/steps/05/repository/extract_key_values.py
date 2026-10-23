import os
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
) -> None:
    """
    Extracts key-value pairs from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us" or "eu").
        processor_id: The ID of the form parser processor.
        file_path: The path to the document file.
    """

    # Initialize client that will be used to send requests. This client only needs to be created
    # once, and can be reused for multiple requests.
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    # You must create a processor before running this sample.
    processor_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"  # Adjust mime_type as needed
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    print(f"Document processing complete. Detected {len(document.form_fields)} form fields.")

    for field in document.form_fields:
        field_name = field.field_name.text_anchor.content if field.field_name else ""
        field_value = field.field_value.text_anchor.content if field.field_value else ""
        print(f"  Field: {field_name}, Value: {field_value}")

if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID")  # A Form Parser Processor
    DOCUMENT_PATH = "path/to/your/form_document.pdf" # Replace with your document path

    if not PROJECT_ID or not PROCESSOR_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_DOCUMENTAI_PROCESSOR_ID environment variables.")
    else:
        # Create a dummy PDF for demonstration purposes if it doesn't exist
        # In a real scenario, you would point to an actual form document.
        if not os.path.exists(DOCUMENT_PATH):
            print(f"Creating a dummy PDF at {DOCUMENT_PATH} for demonstration. "
                  "Please replace this with your actual form document.")
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas

                c = canvas.Canvas(DOCUMENT_PATH, pagesize=letter)
                c.drawString(100, 750, "Name: John Doe")
                c.drawString(100, 730, "Address: 123 Main St")
                c.drawString(100, 710, "City: Anytown")
                c.save()
            except ImportError:
                print("reportlab not installed. Cannot create dummy PDF. Please install it (`pip install reportlab`) "
                      "or provide a real PDF at the specified path.")
                exit(1)

        extract_key_values_from_document(
            project_id=PROJECT_ID,
            location=LOCATION,
            processor_id=PROCESSOR_ID,
            file_path=DOCUMENT_PATH,
        )
