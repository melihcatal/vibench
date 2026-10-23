from google.cloud import documentai_v1 as documentai
import os

def extract_layout_from_document(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> documentai.Document:
    """Extracts layout elements (blocks, lines) from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the general processor (e.g., "OCR_PROCESSOR_ID").
        file_content: The content of the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

    Returns:
        A Document object containing the extracted layout information.
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    # Refer to https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors/process
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)
    return result.document

if __name__ == '__main__':
    # Example usage placeholder
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    # location = "us"
    # processor_id = "your-general-processor-id"  # e.g., an OCR processor
    # with open("path/to/document.pdf", "rb") as f:
    #     content = f.read()
    # doc = extract_layout_from_document(project_id, location, processor_id, content, "application/pdf")
    # print(f"Document Text: {doc.text[:200]}...")
    # print(f"Number of pages: {len(doc.pages)}")
    pass
