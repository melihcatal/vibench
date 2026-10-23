from google.cloud import documentai_v1 as documentai

from document_client import documentai_client, documentai_raw_document, get_env, processor_name
from document_models import KeyValueResponse, OCRRequest


def extract_key_values(request: OCRRequest) -> KeyValueResponse:
    client = documentai_client()
    name = processor_name(get_env("GOOGLE_CLOUD_PROJECT", ""), get_env("GOOGLE_CLOUD_LOCATION", "us"), get_env("GOOGLE_CLOUD_DOCUMENTAI_FORM_PROCESSOR_ID", ""))
    raw = documentai_raw_document(request.image_uri, request.image_bytes)
    result = client.process_document(name=name, raw_document=raw)
    document = result.document
    fields = {}
    for entity in document.entities:
        fields[entity.type_] = entity.mention_text
    return KeyValueResponse(fields=fields, raw={"provider": "google_document_ai", "document": document.to_json()})
