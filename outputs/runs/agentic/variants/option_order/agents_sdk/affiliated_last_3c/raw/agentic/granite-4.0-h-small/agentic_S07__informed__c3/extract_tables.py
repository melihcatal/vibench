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

def extract_tables_from_image(image_bytes: bytes):
    """Extract table cells and row structure from a document using Textract AnalyzeDocument (Forms)."""
    resp = client.analyze_document(Document={"Bytes": image_bytes}, FeatureRequests=[{"Type": "FORMS"}])
    tables = []
    for block in resp.get("Blocks", []):
        if block["BlockType"] == "TABLE":
            rows = []
            for child in block.get("Children", []):
                if child["BlockType"] == "CELL":
                    rows.append(child["Text"])  # simplified flat row text
            tables.append({"rows": rows})
    return tables
