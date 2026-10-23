from google.cloud import documentai_v1 as documentai  # Provider-identifying signal
from google.cloud import storage  # For GCS URI handling


def run_ocr_on_document(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
) -> documentai.Document:
    """Runs OCR on a stored document object using Google Document AI."""
    # You can also use a regional endpoint like "us-documentai.googleapis.com"
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    name = client.processor_path(project_id, location, processor_id)

    # The Document AI SDK expects an InputConfig object
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri)
    input_config = documentai.DocumentInputConfig(gcs_document=gcs_document)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, input_config=input_config)

    result = client.process_document(request=request)
    return result.document
