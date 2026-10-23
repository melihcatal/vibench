from document_client import DocumentClient
from document_models import DocumentPayload, ExtractionResult
import os

def extract_key_values(payload: DocumentPayload, config=None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    client_wrapper = DocumentClient(region_name=region)
    client = client_wrapper.get_textract_client()

    response = client.analyze_document(
        Document={
            "Bytes": payload.document_bytes
        },
        FeatureTypes=["FORMS"]
    )

    key_value_pairs = [block for block in response["Blocks"] if block["BlockType"] == "KEY_VALUE_SET"]

    return ExtractionResult({"key_value_pairs": key_value_pairs}).data
