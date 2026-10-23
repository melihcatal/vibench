from google.cloud import documentai_v1 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str):
    """
    Extracts key-value pairs from a document using Google Cloud Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of your Document AI processor.
        file_path: The local path to the document.
        mime_type: The MIME type of the document (e.g., "application/pdf").
    """

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for entity in document.entities:
        if entity.type == "form_field":
            key = entity.mention_text
            value = ""
            if entity.page_anchor.page_refs:
                for page_ref in entity.page_anchor.page_refs:
                    # Assuming a simple case where value is also a mention_text
                    # For more complex cases, you might need to iterate through entity.properties
                    # or analyze entity.text_anchor
                    for text_segment in page_ref.text_segments:
                        value += document.text[text_segment.start_index:text_segment.end_index]
            key_value_pairs.append({"key": key, "value": value.strip()})

    return key_value_pairs

if __name__ == "__main__":
    # Example usage:
    # Replace with your actual project_id, location, processor_id, file_path, and mime_type
    PROJECT_ID = "your-project-id"
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "your-processor-id"  # e.g., "form-parser-v1"
    FILE_PATH = "path/to/your/document.pdf"
    MIME_TYPE = "application/pdf"

    # extracted_data = extract_key_values(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH, MIME_TYPE)
    # print(extracted_data)
