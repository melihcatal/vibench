import os
from google.cloud import documentai_v1 as documentai
from storage_models import OcrResult


def ocr_document(
    project_id: str, location: str, processor_id: str, gcs_uri: str
) -> OcrResult:
    """
    Performs OCR on a document stored in Google Cloud Storage using Document AI.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.

    :param project_id: Google Cloud project ID.
    :param location: Location of the Document AI processor.
    :param processor_id: ID of the Document AI processor.
    :param gcs_uri: The GCS URI of the document to process (e.g., "gs://bucket_name/file_name.pdf").
    :return: An OcrResult containing the extracted text.
    """

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type="application/pdf")

    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    name = client.processor_path(project_id, location, processor_id)

    request = documentai.ProcessRequest(
        name=name,
        input_documents=input_config,
        skip_human_review=True,
    )

    result = client.process_document(request=request)
    document = result.document

    return OcrResult(text=document.text)
