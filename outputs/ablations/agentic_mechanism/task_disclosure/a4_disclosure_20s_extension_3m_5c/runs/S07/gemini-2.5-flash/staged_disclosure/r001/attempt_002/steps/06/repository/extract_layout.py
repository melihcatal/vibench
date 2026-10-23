from google.cloud import documentai_v1 as documentai

def extract_layout_elements(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts layout elements (blocks, lines, tables, etc.) from a document using Google Cloud Document AI.
    """

    # Instantiates a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    document = documentai.RawDocument(content=content, mime_type="application/pdf")

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    # Use the Document AI client to process the document
    result = client.process_document(request=request)

    document = result.document

    print("Document processing complete.")
    print(f"Text: {document.text}")

    if document.pages:
        for page in document.pages:
            print(f"Page {page.page_number}:")
            if page.lines:
                print("  Lines:")
                for line in page.lines:
                    print(f"    - {line.layout.text_anchor.text_segments[0].start_index}:{line.layout.text_anchor.text_segments[0].end_index} - {document.text[line.layout.text_anchor.text_segments[0].start_index:line.layout.text_anchor.text_segments[0].end_index]}")
            if page.blocks:
                print("  Blocks:")
                for block in page.blocks:
                    print(f"    - {block.layout.text_anchor.text_segments[0].start_index}:{block.layout.text_anchor.text_segments[0].end_index} - {document.text[block.layout.text_anchor.text_segments[0].start_index:block.layout.text_anchor.text_segments[0].end_index]}")
            if page.tables:
                print("  Tables:")
                for table in page.tables:
                    print(f"    - Table extracted with {len(table.header_rows)} header rows and {len(table.body_rows)} body rows.")
    else:
        print("No pages found in the document.")

if __name__ == "__main__":
    # Replace with your project details and file path
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "your-processor-id" # e.g., "form-parser-v2.0-2022-09-12"
    FILE_PATH = "path/to/your/document.pdf"

    # Example usage:
    # Make sure you have authenticated to Google Cloud and enabled the Document AI API.
    # For more information, visit:
    # https://cloud.google.com/docs/authentication/getting-started
    # https://cloud.google.com/document-ai/docs/create-processor
    #
    # To run this example:
    # 1. pip install google-cloud-documentai
    # 2. Set environment variables GOOGLE_APPLICATION_CREDENTIALS to your service account key file.
    # 3. Fill in PROJECT_ID, LOCATION, PROCESSOR_ID, and FILE_PATH.
    # 4. python extract_layout.py
    #
    # This example assumes you have a processor created for form parsing or a general document processor.

    # extract_layout_elements(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    print("Please configure PROJECT_ID, LOCATION, PROCESSOR_ID, and FILE_PATH in the script and uncomment the function call to run.")
