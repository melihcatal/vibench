import os
import boto3
from document_client import DocumentClient
from document_models import OCRResult

# Amazon Textract
client = boto3.client(
    "textract",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def extract_layout_from_image(image_bytes: bytes) -> LayoutResult:
    """Extract layout elements (lines, words, tables) from a document image using Textract."""
    resp = client.analyze_document(Document={"Bytes": image_bytes}, FeatureRequests=[{"Type": "FORMS"}])
    # Simplify: collect all LINE and WORD blocks
    blocks = [
        Block(text=block["Text"], type_=block["BlockType"])
        for block in resp.get("Blocks", [])
        if block["BlockType"] in {"LINE", "WORD"}
    ]
    return LayoutResult(blocks=blocks)
