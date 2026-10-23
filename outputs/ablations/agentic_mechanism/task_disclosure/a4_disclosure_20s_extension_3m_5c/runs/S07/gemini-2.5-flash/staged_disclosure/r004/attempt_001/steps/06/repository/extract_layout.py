import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_document_layout(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Extracts layout information from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the Document AI processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A Document object containing the extracted layout information.
    """

    # You must set the api_endpoint if your processor is not in the default global region
    # For example, "us-documentai.googleapis.com" for a processor in the "us" region
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == "__main__":
    # Replace with your actual project ID, location, and processor ID
    PROJECT_ID = "YOUR_PROJECT_ID"
    LOCATION = "YOUR_LOCATION"  # e.g., "us"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # e.g., "a1b2c3d4e5f6g7h8"
    FILE_PATH = "path/to/your/document.pdf"  # Replace with your document path
    MIME_TYPE = "application/pdf" # Replace with your document's MIME type

    if PROJECT_ID == "YOUR_PROJECT_ID" or LOCATION == "YOUR_LOCATION" or PROCESSOR_ID == "YOUR_PROCESSOR_ID":
        print("Please replace 'YOUR_PROJECT_ID', 'YOUR_LOCATION', and 'YOUR_PROCESSOR_ID' with your actual Google Cloud Document AI credentials and document path.")
    else:
        print(f"Extracting layout from {FILE_PATH} using Document AI...")
        try:
            document = extract_document_layout(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, MIME_TYPE)
            print("Document layout extracted successfully!")
            # You can now process the 'document' object to access blocks, lines, tables, etc.
            # For example, to print the text:
            # print("Full document text:")
            # print(document.text)
        except Exception as e:
            print(f"Error extracting document layout: {e}")
