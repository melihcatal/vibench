
from google.cloud import documentai_v1 as documentai

def extract_layout_elements(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts layout elements from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The location of the processor (e.g., "us").
        processor_id: The ID of the Document AI processor.
        file_path: The path to the document file.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf"  # Or other appropriate mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request)

    document = result.document
    print(f"Document processing complete. Text: {document.text}\n")

    for page in document.pages:
        print(f"Page {page.page_number}:")
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content if form_field.field_name.text_anchor else ""
            field_value = form_field.field_value.text_anchor.content if form_field.field_value.text_anchor else ""
            print(f"  Form Field: Name: {field_name}, Value: {field_value}")

        for entity in document.entities:
            print(f"  Entity: Type: {entity.type_}, Mention Text: {entity.mention_text}")

        for block in page.blocks:
            print(f"  Block: {block.layout.text_anchor.content}")

        for paragraph in page.paragraphs:
            print(f"  Paragraph: {paragraph.layout.text_anchor.content}")

        for line in page.lines:
            print(f"  Line: {line.layout.text_anchor.content}")

        for table in page.tables:
            print(f"  Table with {len(table.header_rows)} header rows and {len(table.body_rows)} body rows.")
            for row_num, row in enumerate(table.header_rows):
                print(f"    Header Row {row_num}:")
                for cell_num, cell in enumerate(row.cells):
                    print(f"      Cell {cell_num}: {cell.layout.text_anchor.content}")
            for row_num, row in enumerate(table.body_rows):
                print(f"    Body Row {row_num}:")
                for cell_num, cell in enumerate(row.cells):
                    print(f"      Cell {cell_num}: {cell.layout.text_anchor.content}")


if __name__ == "__main__":
    # Replace with your Google Cloud project details
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us" or "eu"
    PROCESSOR_ID = "your-processor-id"  # Create a "Form Parser" or "OCR" processor in Document AI
    FILE_PATH = "path/to/your/document.pdf"  # Replace with the path to your document

    print("Make sure you have authenticated to Google Cloud. For example:")
    print("gcloud auth application-default login")
    print(f"Then create a Document AI processor (e.g., 'Form Parser' or 'OCR') in the '{LOCATION}' location.")
    print(f"And enable the Document AI API.")
    print(f"Example usage: extract_layout_elements(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)")

    # Uncomment the line below to run the extraction
    # extract_layout_elements(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
