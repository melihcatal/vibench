import os
import json
from google.cloud import documentai_v1 as documentai
from storage_client import ManagedStorageClient


def ocr_stored_document(bucket_name: str, object_key: str) -> dict:
    """Run OCR on a PDF/image stored in managed object storage using Google Document AI.

    Returns a structured dict with extracted text and entity annotations.
    """
    client = ManagedStorageClient.get_s3_client()
    # Fetch the raw bytes of the document from S3
    try:
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        document_bytes = response["Body"].read()
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve document: {e}")

    # Prepare the Document AI request (PDF as bytes)
    processor_uri = os.getenv(
        "DOCUMENT_AI_PROCESSOR_URI"
    )  # e.g., projects/123/locations/us/processors/abc
    processor_type = "document"  # PDF/IMAGE processing

    document = documentai.types.Document(
        content=document_bytes, mime_type="application/pdf"
    )

    # Call the Document AI service (requires Google credentials via GOOGLE_APPLICATION_CREDENTIALS)
    client_service = documentai.DocumentProcessorServiceClient()
    request = documentai.types.ProcessDocumentRequest(
        name=processor_uri,
        document=document,
        output_config={"gcs_destination": {"uri": f"gs://temp-bucket/ocr-output"}},
    )
    operation = client_service.process_document(request=request)
    result = operation.result(timeout=120)
    # Simplify response: extract full text and entities
    extracted_text = "\n".join(
        result.document.pages[0].layout[0].text if result.document.pages else ""
    )
    entities = [
        {
            "type": e.type_,
            "mention_text": e.mention_text,
            "bounding_poly": e.bounding_poly.normalized_vertices,
        }
        for e in result.document.entities
    ]
    return {
        "extracted_text": extracted_text,
        "entities": entities,
    }
