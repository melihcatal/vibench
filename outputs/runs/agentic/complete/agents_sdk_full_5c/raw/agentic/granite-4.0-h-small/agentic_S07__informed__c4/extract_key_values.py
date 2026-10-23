import os
import re
from google.cloud import documentai_v1 as documentai

# Use Google Cloud Document AI for KV extraction (prebuilt form processor)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(PROJECT_ID, LOCATION, "form-processor")

def extract_key_values(image_bytes):
    client = documentai.DocumentProcessorServiceClient()
    raw_document = documentai.RawDocument(content=image_bytes, mime_type="image/png")
    input_config = documentai.InputConfig(raw_document=raw_document)
    request = documentai.ProcessRequest(name=PROCESSOR_ID, input_config=input_config)
    result = client.process_document(request=request)
    kv = {}
    for entity in result.document.entities:
        # Simple heuristic: treat any non-label field as a value and nearest label as key
        if entity.type_ == "LABEL_DETECTION":
            key = entity.text_anchor.content.strip()
        elif entity.type_ == "OTHER":
            value = entity.text_anchor.content.strip()
            kv[key] = value
    return kv
