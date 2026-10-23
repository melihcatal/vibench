import os
from google.cloud import documentai


def ocr_document_from_gcs(
    gcs_uri: str, mime_type: str = "application/pdf"
) -> documentai.Document:
    """
    Performs OCR on a document stored in Google Cloud Storage using Document AI.

    Args:
        gcs_uri: The GCS URI of the document (e.g., gs://bucket_name/file_name).
        mime_type: The MIME type of the document.

    Returns:
        A Document AI Document object containing the OCR results.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError(
            "GCP_PROJECT_ID, GCP_LOCATION, and DOCUMENT_AI_PROCESSOR_ID must be set."
        )

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    gcs_source = documentai.GcsSource(uri=gcs_uri)
    input_config = documentai.DocumentOutputConfig.GcsOutputConfig(
        gcs_uri=gcs_source.uri
    )

    request = documentai.ProcessRequest(
        name=client.processor_path(project_id, location, processor_id),
        gcs_document=gcs_document,
        document_output_config=input_config,
    )

    result = client.process_document(request=request)
    return result.document
