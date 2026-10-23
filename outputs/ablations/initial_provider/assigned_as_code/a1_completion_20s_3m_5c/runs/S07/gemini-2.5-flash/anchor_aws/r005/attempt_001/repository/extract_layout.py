from document_client import DocumentClient
from document_models import DocumentPayload, ExtractionResult
import os

def extract_layout(payload: DocumentPayload, config=None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    client_wrapper = DocumentClient(region_name=region)
    client = client_wrapper.get_textract_client()

    response = client.analyze_document(
        Document={
            "Bytes": payload.document_bytes
        },
        FeatureTypes=["LAYOUT"]
    )

    layout_blocks = [block for block in response["Blocks"] if block["BlockType"] in ["PAGE", "WORD", "LINE", "TABLE", "CELL", "MERGED_CELL", "TITLE", "PARAGRAPH", "LIST", "LIST_ITEM", "KEY_VALUE_SET"]]

    return ExtractionResult({"layout_blocks": layout_blocks}).data
