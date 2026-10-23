import os

from google.cloud import documentai

from storage_client import get_bucket_name, get_client


def stored_document_ocr(
    bucket_name: str | None,
    object_name: str,
    project_id: str,
    location: str,
    processor_id: str,
) -> str:
    storage_client = get_client()
    blob = storage_client.bucket(get_bucket_name(bucket_name)).blob(object_name)
    docai = documentai.DocumentProcessorServiceClient()
    name = docai.processor_path(project_id, location, processor_id)
    gcs_document = documentai.GcsDocument(
        gcs_uri=f"gs://{blob.bucket.name}/{blob.name}",
        mime_type=blob.content_type or "application/pdf",
    )
    request = documentai.ProcessRequest(
        name=name,
        gcs_document=documentai.GcsDocument(
            gcs_uri=gcs_document.gcs_uri, mime_type=gcs_document.mime_type
        ),
    )
    return docai.process_document(request=request).document.text


if __name__ == "__main__":
    print(
        stored_document_ocr(
            os.getenv("STORAGE_BUCKET"),
            os.environ["OBJECT_NAME"],
            os.environ["DOCUMENTAI_PROJECT_ID"],
            os.environ["DOCUMENTAI_LOCATION"],
            os.environ["DOCUMENTAI_PROCESSOR_ID"],
        )
    )
