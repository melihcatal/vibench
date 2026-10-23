import os
from google.cloud import documentai
from google.cloud.documentai_v1 import (
    DocumentProcessorServiceClient,
    ProcessRequest,
    RawDocument,
)
from document_models import KVResponse

project_id = os.getenv("GOOGLE_PROJECT_ID")
location = "us"
processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")

client = DocumentProcessorServiceClient()
name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def extract_key_values(image_path: str) -> KVResponse:
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()
    raw_document = RawDocument(content=image_content, mime_type="image/jpeg")
    request = ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    pairs = []
    for entity in document.entities:
        pairs.append({"key": entity.type_, "value": entity.mention_text})
    return {"pairs": pairs}
