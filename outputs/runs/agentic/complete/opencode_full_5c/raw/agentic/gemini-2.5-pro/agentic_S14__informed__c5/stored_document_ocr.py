import os
from google.cloud import documentai


def ocr_stored_document(
    gcs_uri: str,
    processor_id: str,
    project_id: str,
    location: str = "us",
) -> str:
    """
    Performs OCR on a document stored in Google Cloud Storage using Document AI.

    :param gcs_uri: The GCS URI of the document (e.g., gs://bucket_name/file_name).
    :param processor_id: The ID of the Document AI processor.
    :param project_id: The Google Cloud project ID.
    :param location: The location of the processor.
    :return: The extracted text from the document.
    """
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type="application/pdf")
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    name = client.processor_path(project_id, location, processor_id)

    request = documentai.ProcessRequest(name=name, input_documents=input_config)
    result = client.process_document(request=request)

    return result.document.text
