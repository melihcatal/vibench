from google.cloud import documentai_v1 as documentai
import os

def get_document_ai_client():
    """Returns a Google Document AI client."""
    # The client automatically picks up GOOGLE_APPLICATION_CREDENTIALS
    # from the environment or well-known locations.
    return documentai.DocumentProcessorServiceClient()

def get_document_content(file_path: str, mime_type: str = "application/pdf"):
    """Reads a file and returns it as a Document AI RawDocument."""
    with open(file_path, "rb") as image:
        image_content = image.read()
    return documentai.RawDocument(content=image_content, mime_type=mime_type)

def create_processor_name(project_id: str, location: str, processor_id: str):
    """Creates a fully qualified processor name."""
    client = get_document_ai_client()
    return client.processor_path(project_id, location, processor_id)

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS set up)
    # client = get_document_ai_client()
    # print(f"Document AI client initialized: {client}")
    pass
