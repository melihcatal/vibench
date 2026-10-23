from document_client import DocumentClient
from document_models import DocumentPayload, ExtractionResult
import os

def extract_tables(payload: DocumentPayload, config=None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    client_wrapper = DocumentClient(region_name=region)
    client = client_wrapper.get_textract_client()

    response = client.analyze_document(
        Document={
            "Bytes": payload.document_bytes
        },
        FeatureTypes=["TABLES"]
    )

    table_blocks = [block for block in response["Blocks"] if block["BlockType"] == "TABLE"]

    return ExtractionResult({"table_blocks": table_blocks}).data
