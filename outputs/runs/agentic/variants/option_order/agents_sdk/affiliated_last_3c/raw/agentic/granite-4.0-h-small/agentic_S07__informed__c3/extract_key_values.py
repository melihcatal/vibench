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

def extract_key_values_from_image(image_bytes: bytes):
    """Extract key-value pairs from a form-like document using Textract AnalyzeDocument (Forms)."""
    resp = client.analyze_document(Document={"Bytes": image_bytes}, FeatureRequests=[{"Type": "FORMS"}])
    kv_pairs = {}
    for block in resp.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET":
            kv_type = block.get("KeyValueSetType")
            if kv_type == "KEY":
                key = block["Text"]
            elif kv_type == "VALUE":
                value = block["Text"]
                if key:
                    kv_pairs[key] = value
                    key = ""  # reset after pairing
    return kv_pairs
