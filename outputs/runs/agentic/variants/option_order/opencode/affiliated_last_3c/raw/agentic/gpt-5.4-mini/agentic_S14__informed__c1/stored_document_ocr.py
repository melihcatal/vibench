import os

from google.cloud import documentai

from storage_client import load_storage_config
from storage_models import normalize_object_name


def run_document_ocr(
    object_name: str, project_id: str, location: str, processor_id: str
):
    config = load_storage_config()
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    gcs_source = documentai.GcsDocument(
        gcs_uri=f"gs://{config.bucket_name}/{normalize_object_name(object_name)}",
        mime_type="application/pdf",
    )
    request = documentai.ProcessRequest(
        name=name,
        gcs_document=documentai.GcsDocument(
            gcs_uri=gcs_source.gcs_uri, mime_type=gcs_source.mime_type
        ),
    )
    result = client.process_document(request=request)
    return result.document.text
