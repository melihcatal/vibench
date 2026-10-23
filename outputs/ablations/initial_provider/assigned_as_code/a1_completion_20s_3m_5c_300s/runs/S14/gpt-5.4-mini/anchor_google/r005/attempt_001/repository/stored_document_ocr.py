from google.cloud import documentai

from storage_client import storage_client


def stored_document_ocr(payload, config=None):
    client, config = storage_client(config)
    storage_bucket = client.bucket(config["bucket"])
    blob = storage_bucket.blob(payload["object_name"])
    documentai_client = documentai.DocumentProcessorServiceClient()
    processor_name = documentai_client.processor_path(config["project_id"], config["location"], config["processor_id"])
    content = blob.download_as_bytes()
    request = documentai.ProcessRequest(name=processor_name, raw_document=documentai.RawDocument(content=content, mime_type=payload.get("content_type", blob.content_type or "application/pdf")))
    result = documentai_client.process_document(request=request)
    return {"text": result.document.text, "object_name": payload["object_name"]}
