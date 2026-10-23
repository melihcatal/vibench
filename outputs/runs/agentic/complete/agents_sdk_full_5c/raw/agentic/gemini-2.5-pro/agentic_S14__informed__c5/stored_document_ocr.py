import os
from google.cloud import documentai

def ocr_stored_document(gcs_uri: str, mime_type: str = "application/pdf") -> str:
    """
    Processes a document stored in Google Cloud Storage using the Document AI API.
    
    :param gcs_uri: The GCS URI of the document (e.g., "gs://your-bucket/your-file.pdf").
    :param mime_type: The MIME type of the document.
    :return: The extracted text content of the document.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("DOCUMENT_AI_LOCATION", "us")  # e.g., 'us' or 'eu'
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Required environment variables for Document AI are not set.")

    # You must set the `api_endpoint` if you use a location other than 'us', e.g.:
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    name = client.processor_path(project_id, location, processor_id)

    # Configure the process request
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    request = documentai.ProcessRequest(
        name=name,
        input_documents=input_config,
        skip_human_review=True,
    )
    
    result = client.process_document(request=request)
    document = result.document

    print(f"Document processing complete for {gcs_uri}.")
    return document.text
