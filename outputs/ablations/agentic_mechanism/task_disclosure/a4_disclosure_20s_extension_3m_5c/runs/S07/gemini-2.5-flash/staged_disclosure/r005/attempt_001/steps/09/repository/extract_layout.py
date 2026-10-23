from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_layout_from_document(
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

    # Online processing support only a single file
    document = None
    documentai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary into a Document
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    name = documentai_client.processor_path(project_id, location, processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = documentai_client.process_document(request=request)
    document = result.document

    return document

if __name__ == "__main__":
    # This is example usage. Replace with your actual project details and file.
    # For example, you would typically get these values from environment variables
    # or a configuration file.
    PROJECT_ID = "your-project-id"  # TODO: Replace with your project ID
    LOCATION = "us"  # TODO: Replace with your processor location
    PROCESSOR_ID = "your-processor-id"  # TODO: Replace with your processor ID
    FILE_PATH = "path/to/your/document.pdf"  # TODO: Replace with your document path
    MIME_TYPE = "application/pdf"  # TODO: Replace with your document MIME type

    # Example of how to call the function
    # Make sure to install the Google Cloud Document AI client library:
    # pip install google-cloud-documentai

    try:
        # extracted_document = extract_layout_from_document(
        #     PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, MIME_TYPE
        # )

        # print(f"Document processing complete.")
        # print(f"Text: {extracted_document.text}")

        # For a more detailed breakdown of what's in the document object,
        # you would iterate through its entities, pages, etc.
        # For example, to print block information:
        # for page in extracted_document.pages:
        #     for block in page.blocks:
        #         print(f"Block Bounding Box: {block.layout.bounding_poly}")
        #         print(f"Block Text: {extracted_document.text[block.layout.text_anchor.start_index:block.layout.text_anchor.end_index]}")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")

