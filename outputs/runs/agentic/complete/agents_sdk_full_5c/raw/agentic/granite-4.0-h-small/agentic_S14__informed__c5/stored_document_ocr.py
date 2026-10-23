import os
import mindee
from mindee import MindeeClient

def ocr_document_from_gcs(bucket_name, blob_name, mindee_api_key):
    """Run OCR on a PDF stored in Google Cloud Storage using Mindee Document OCR."
    # Initialize client using env var MINDEE_API_KEY or pass directly
    client = MindeeClient(api_key=mindee_api_key)
    # Download PDF bytes from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    pdf_bytes = blob.download_as_bytes()
    # Send PDF to Mindee OCR API (v3 Invoice API works for generic docs)
    result = client.parse(pdf=pdf_bytes, product='mindee/document_v3')
    # Return extracted structured data as dict
    return {
        "text": result.text,
        "fields": result.document_fields,
        "confidence": result.confidence,
    }
