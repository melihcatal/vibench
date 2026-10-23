import os
from google.cloud import documentai_v1 as documentai

# Metadata field extraction (structured fields from OCR-normalized text)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(PROJECT_ID, LOCATION, "form-processor")

def extract_document_fields(ocr_text):
    client = documentai.DocumentProcessorServiceClient()
    raw_document = documentai.RawDocument(content=ocr_text.encode('utf-8'), mime_type="text/plain")
    input_config = documentai.InputConfig(raw_document=raw_document)
    request = documentai.ProcessRequest(name=PROCESSOR_ID, input_config=input_config)
    result = client.process_document(request=request)
    # Assume the processor returns a structured form with fields
    fields = {}
    for entity in result.document.entities:
        if entity.HasField("field"):
            fields[entity.name] = entity.field.value.text_anchor.content
    return fields
