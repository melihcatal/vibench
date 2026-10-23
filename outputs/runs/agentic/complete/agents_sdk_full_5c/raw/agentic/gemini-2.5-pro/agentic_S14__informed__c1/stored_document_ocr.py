import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

def ocr_gcs_document(gcs_uri: str, mime_type: str = "application/pdf") -> str:
    """
    Performs OCR on a document stored in Google Cloud Storage using Document AI.

    Args:
        gcs_uri (str): The GCS URI of the document (e.g., gs://bucket/file.pdf).
        mime_type (str): The MIME type of the document.

    Returns:
        str: The extracted text from the document.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.environ.get("GCP_DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("GCP_PROJECT_ID, GCP_DOCUMENT_AI_LOCATION, and GCP_DOCUMENT_AI_PROCESSOR_ID must be set.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, gcs_document=gcs_document)

    result = client.process_document(request=request)
    
    document = result.document
    return document.text
