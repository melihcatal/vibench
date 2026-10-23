import os
from google.cloud import documentai_v1beta3 as documentai

def extract_tables(image_content: bytes, project_id: str, location: str, processor_id: str) -> documentai.Document:
    """Extracts table cells and row structure from a document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF for tables

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    response = client.process_document(request=request)

    # The response.document object contains the extracted tables within its pages.
    return response.document

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _location = "us"
    _processor_id = os.environ.get("DOCUMENT_AI_TABLE_PROCESSOR_ID", "your-table-processor-id") # Replace with your table processor ID

    _dummy_pdf_content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj\n4 0 obj<</Length 11>>stream\nBT /F1 12 Tf ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000059 00000 n\n0000000109 00000 n\n0000000216 00000 n\ntrailer<</Size 5/Root 1 0 R>>startxref\n277\n%%EOF"
    print(f"Using Document AI Table Processor: {_processor_id}")
    # _document = extract_tables(_dummy_pdf_content, _project_id, _location, _processor_id)
    # if _document and _document.pages:
    #     for page in _document.pages:
    #         for table in page.tables:
    #             print(f"Found table with {len(table.header_rows)} header rows and {len(table.body_rows)} body rows.")
    print("Table extraction example is commented out. Provide a real PDF and credentials to run.")
