from document_client import load_document_input, s3_object_reference, textract_client
from document_models import KeyValueExtractionResult, kv_from_textract


def extract_key_values(bucket: str | None = None, key: str | None = None, version: str | None = None) -> KeyValueExtractionResult:
    bucket, key, version = load_document_input(bucket, key, version)
    response = textract_client().analyze_document(Document=s3_object_reference(bucket, key, version), FeatureTypes=["FORMS"])
    return KeyValueExtractionResult(key_values=kv_from_textract(response.get("Blocks", [])), raw=response)
