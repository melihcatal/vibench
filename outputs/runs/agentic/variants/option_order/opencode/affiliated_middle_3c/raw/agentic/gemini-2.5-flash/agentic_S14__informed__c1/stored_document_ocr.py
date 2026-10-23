import os
from google.cloud import documentai_v1 as documentai


# Google Cloud Document AI client
def get_document_ai_client():
    """
    Provides a Google Document AI client.
    Authenticates using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return documentai.DocumentProcessorServiceClient()


def run_ocr_on_stored_document(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
) -> str:
    """
    Runs OCR on a stored document object using Google Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., 'us').
        processor_id: The ID of the Document AI processor to use.
        gcs_input_uri: The Google Cloud Storage URI of the input document (e.g., 'gs://bucket/path/to/document.pdf').

    Returns:
        The extracted text content from the document.
    """
    client = get_document_ai_client()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Configure the process request
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri)
    input_config = documentai.DocumentInputConfig(gcs_document=gcs_document)

    request = documentai.ProcessRequest(name=name, input_config=input_config)

    result = client.process_document(request=request)
    document = result.document

    return document.text
