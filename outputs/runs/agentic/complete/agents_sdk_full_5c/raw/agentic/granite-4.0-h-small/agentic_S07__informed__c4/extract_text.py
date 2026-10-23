import os
from google.cloud import documentai_v1 as documentai

# Use Document AI OCR processor (supports plain text extraction from scanned images)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"  # or "eu"
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(PROJECT_ID, LOCATION, "doc-ocr")

def extract_text_from_image(image_bytes):
    client = documentai.DocumentProcessorServiceClient()
    # prepare request
    raw_document = documentai.RawDocument(content=image_bytes, mime_type="image/png")
    input_config = documentai.InputConfig(raw_document=raw_document)
    request = documentai.ProcessRequest(name=PROCESSOR_ID, input_config=input_config)
    # call API
    result = client.process_document(request=request)
    # extract plain text
    document = result.document
    text = document.text
    return text
