from document_client import load_document_input, s3_object_reference, textract_client
from document_models import TableExtractionResult


def extract_tables(bucket: str | None = None, key: str | None = None, version: str | None = None) -> TableExtractionResult:
    bucket, key, version = load_document_input(bucket, key, version)
    response = textract_client().analyze_document(Document=s3_object_reference(bucket, key, version), FeatureTypes=["TABLES"])
    tables = [b for b in response.get("Blocks", []) if b.get("BlockType") == "TABLE"]
    return TableExtractionResult(tables=tables, raw=response)
