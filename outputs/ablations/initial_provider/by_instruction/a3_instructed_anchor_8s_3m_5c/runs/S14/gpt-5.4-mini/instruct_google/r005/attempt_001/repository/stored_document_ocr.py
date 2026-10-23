from google.cloud import documentai

from storage_client import get_bucket, get_object_path
from storage_models import OcrResult


def stored_document_ocr(bucket: str, key: str, project_id: str, location: str, processor_id: str) -> OcrResult:
    bucket_client = get_bucket(bucket)
    blob = bucket_client.blob(get_object_path(key))
    document = documentai.RawDocument(content=blob.download_as_bytes(), mime_type=blob.content_type or "application/pdf")
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=document)
    result = client.process_document(request=request)
    text = result.document.text or ""
    return OcrResult(bucket=bucket, key=key, text=text)
