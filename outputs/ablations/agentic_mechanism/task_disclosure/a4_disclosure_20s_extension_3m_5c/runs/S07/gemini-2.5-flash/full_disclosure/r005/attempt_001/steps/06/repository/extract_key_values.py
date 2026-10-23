from google.cloud import documentai_v1beta3 as documentai
import os

def extract_key_value_pairs(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    file_mime_type: str,
) -> dict:
    """
    Extracts key-value pairs from a document using Google Cloud Document AI's Form Parser.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the processor (e.g., "us").
        processor_id (str): The ID of the Form Parser processor.
        file_path (str): The path to the document file.
        file_mime_type (str): The MIME type of the document (e.g., "application/pdf").

    Returns:
        dict: A dictionary containing the extracted key-value pairs.
    """

    # You can set the GOOGLE_APPLICATION_CREDENTIALS environment variable or
    # explicitly pass credentials to the client.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.

    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=file_mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_segments[0].content if form_field.field_name.text_segments else ""
            field_value = form_field.field_value.text_segments[0].content if form_field.field_value.text_segments else ""
            if field_name:
                key_value_pairs[field_name.strip()] = field_value.strip()

    return key_value_pairs

