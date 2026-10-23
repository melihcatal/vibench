from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def extract_structured_fields(project_id: str, location: str, processor_id: str, document_content: bytes, mime_type: str):
    """
    Extracts structured fields from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the processor to use (e.g., "YOUR_PROCESSOR_ID").
        document_content: The content of the document as bytes.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A Document object containing the extracted fields.
    """
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with your actual project_id, location, processor_id, and document content.
    # For a real application, you would load your document content from a file or other source.

    # Example: dummy values for demonstration
    # project_id = "your-project-id"
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "your-processor-id"  # e.g., a form parser processor
    # document_content = b"This is some dummy document text for extraction."
    # mime_type = "text/plain"

    # # If you have a PDF, you would read it as bytes:
    # # with open("path/to/your/document.pdf", "rb") as image:
    # #     document_content = image.read()
    # # mime_type = "application/pdf"

    # try:
    #     document = extract_structured_fields(project_id, location, processor_id, document_content, mime_type)
    #     print("Document processing complete.")
    #     # Further processing of the document object to access extracted fields
    #     # For example, to print entities (structured fields):
    #     # if document.entities:
    #     #     for entity in document.entities:
    #     #         print(f"  Entity: {entity.type_}")
    #     #         print(f"    Mention Text: {entity.mention_text}")
    #     #         print(f"    Confidence: {entity.confidence}")
    # except Exception as e:
    #     print(f"Error processing document: {e}")
    pass
