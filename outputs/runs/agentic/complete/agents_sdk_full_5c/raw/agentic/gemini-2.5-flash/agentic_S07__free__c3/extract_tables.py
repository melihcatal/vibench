from google.cloud import documentai_v1 as documentai
import os

def extract_tables_from_document(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> documentai.Document:
    """Extracts table cells and row structure from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of a table parser processor or general processor (e.g., "TABLE_PROCESSOR_ID").
        file_content: The content of the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf", "image/jpeg").

    Returns:
        A Document object containing the extracted table information.
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    # Refer to https://cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors/process
    # Ensure the processor_id is configured for table extraction, e.g., a "Table Parser" processor
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
    # processor_id = "your-table-processor-id"  # or a general processor that supports tables
    # with open("path/to/document_with_tables.pdf", "rb") as f:
    #     content = f.read()
    # doc = extract_tables_from_document(project_id, location, processor_id, content, "application/pdf")
    # print(f"Document Text: {doc.text[:200]}...")
    # if doc.pages:
    #     for i, page in enumerate(doc.pages):
    #         print(f"Page {i+1} has {len(page.tables)} tables.")
    pass
