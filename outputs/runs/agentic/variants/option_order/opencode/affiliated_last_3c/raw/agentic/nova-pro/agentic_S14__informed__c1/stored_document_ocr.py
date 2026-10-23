import os
from google.cloud import documentai


def stored_document_ocr(bucket_name, blob_name):
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = "us"
    processor_id = "YOUR_PROCESSOR_ID"
    processor = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    # Additional code to process the document
    print(f"Performing OCR on {blob_name}")
