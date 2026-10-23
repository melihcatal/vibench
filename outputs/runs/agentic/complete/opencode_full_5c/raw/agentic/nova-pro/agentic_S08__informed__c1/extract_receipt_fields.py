import os
from google.cloud import documentai_v1 as documentai


def extract_receipt_fields(receipt_path):
    client = documentai.DocumentProcessorServiceClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    request = documentai.ProcessDocumentRequest(
        name="projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/processors/YOUR_PROCESSOR_ID",
        raw_document=documentai.RawDocument(content=receipt_path),
    )
    result = client.process_document(request=request)
    return result.document
