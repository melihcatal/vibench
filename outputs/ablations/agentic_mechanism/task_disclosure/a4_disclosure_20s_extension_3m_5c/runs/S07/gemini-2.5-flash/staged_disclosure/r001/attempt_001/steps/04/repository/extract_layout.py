from google.cloud import documentai_v1beta3 as documentai
import os

def extract_layout_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
):
    """
    Extracts blocks, lines, tables, or layout elements from a document using Google Cloud Document AI.
    """

    # You must set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file.
    # For example:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image_file:
        content = image_file.read()

    document = documentai.RawDocument(content=content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=document)

    result = client.process_document(request=request)

    document_response = result.document
    
    # For a list of entities in the document:
    # for entity in document_response.entities:
    #     print(f"Entity type: {entity.type_}")
    #     print(f"Mention text: {entity.mention_text}")

    # For text, pages, and other layout elements:
    # print(f"Document Text: {document_response.text}")
    # for page in document_response.pages:
    #     print(f"Page {page.page_number}:")
    #     for form_field in page.form_fields:
    #         print(f"  Field Name: {form_field.field_name.text_anchor.content}")
    #         print(f"  Field Value: {form_field.field_value.text_anchor.content}")
    #     for paragraph in page.paragraphs:
    #         print(f"  Paragraph: {paragraph.layout.text_anchor.content}")
    #     for block in page.blocks:
    #         print(f"  Block: {block.layout.text_anchor.content}")
    #     for line in page.lines:
    #         print(f"  Line: {line.layout.text_anchor.content}")
    
    return document_response

if __name__ == "__main__":
    # Example usage (replace with your actual values)
    # project_id = "your-gcp-project-id"
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "your-processor-id"  # e.g., "YOUR_PROCESSOR_ID"
    # file_path = "path/to/your/document.pdf"
    # mime_type = "application/pdf"  # e.g., "application/pdf" or "image/tiff"

    # print("Extracting layout from document...")
    # document_layout = extract_layout_from_document(
    #     project_id, location, processor_id, file_path, mime_type
    # )
    # print("Layout extraction complete.")
    # print(document_layout.text) # Prints the full text extracted from the document
