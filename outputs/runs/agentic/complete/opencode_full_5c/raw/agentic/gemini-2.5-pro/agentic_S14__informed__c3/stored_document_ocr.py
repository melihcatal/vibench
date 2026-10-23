import os
from google.cloud import documentai_v1 as documentai


def ocr_stored_document(
    bucket_name: str, object_key: str, project_id: str, location: str, processor_id: str
) -> str:
    """
    Performs OCR on a document stored in Google Cloud Storage using Document AI.

    Args:
        bucket_name: The GCS bucket where the document is stored.
        object_key: The key of the document object in the bucket.
        project_id: Your Google Cloud project ID.
        location: The location of the Document AI processor.
        processor_id: The ID of the Document AI processor.

    Returns:
        The extracted text from the document.
    """
    client = documentai.DocumentProcessorServiceClient()

    gcs_uri = f"gs://{bucket_name}/{object_key}"

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Configure the request
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type="application/pdf")
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    request = documentai.ProcessRequest(
        name=name,
        input_documents=input_config,
    )

    # Make the synchronous call
    result = client.process_document(request=request)

    document = result.document
    return document.text
