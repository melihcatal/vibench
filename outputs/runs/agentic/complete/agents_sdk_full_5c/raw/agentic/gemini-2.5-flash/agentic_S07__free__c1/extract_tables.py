import os
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us"
PROCESSOR_ID_TABLE = os.environ.get("GCP_DOCUMENTAI_TABLE_PROCESSOR_ID") # e.g., "form-parser-v2.1-2023-01-26" or a custom table parser

def extract_tables(image_content: bytes) -> documentai.Document:
    """Extracts table cells and row structure from a document using Google Cloud Document AI Table Parser."""
    if not all([PROJECT_ID, PROCESSOR_ID_TABLE]):
        raise ValueError("Environment variables GCP_PROJECT_ID, GCP_DOCUMENTAI_TABLE_PROCESSOR_ID must be set.")

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    resource_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID_TABLE)

    # Read the file into memory
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Tables often in PDFs

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document

if __name__ == 'main':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and required env vars are set.
    os.environ["GCP_PROJECT_ID"] = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    os.environ["GCP_DOCUMENTAI_TABLE_PROCESSOR_ID"] = os.environ.get("GCP_DOCUMENTAI_TABLE_PROCESSOR_ID", "table-parser") # Use 'table-parser' for the pre-trained table parser

    try:
        with open("example_table.pdf", "rb") as document_file:
            content = document_file.read()
        document = extract_tables(content)
        print("Document Tables found:", sum(len(page.tables) for page in document.pages))
        if document.pages and document.pages[0].tables:
            first_table = document.pages[0].tables[0]
            print(f"First table rows: {len(first_table.header_rows) + len(first_table.body_rows)}")
    except FileNotFoundError:
        print("Please create an 'example_table.pdf' file or replace the path with a valid document.")
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
