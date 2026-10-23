import os
from google.cloud import documentai
from storage_client import get_client


def stored_document_ocr(bucket_name: str, object_name: str) -> str:
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    location = os.getenv('GOOGLE_DOCUMENTAI_LOCATION', 'us')
    processor_id = os.environ['GOOGLE_DOCUMENTAI_PROCESSOR_ID']
    name = client.processor_path(project_id, location, processor_id)
    gcs_uri = f'gs://{bucket_name}/{object_name}'
    request = documentai.ProcessRequest(name=name, gcs_document=documentai.GcsDocument(gcs_uri=gcs_uri, mime_type='application/pdf'))
    result = client.process_document(request=request)
    return result.document.text
