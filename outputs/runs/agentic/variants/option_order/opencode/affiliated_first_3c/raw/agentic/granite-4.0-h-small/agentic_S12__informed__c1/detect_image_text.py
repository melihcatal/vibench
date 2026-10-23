# Detect text appearing inside an image using AWS Textract
import os
import boto3
from vision_client import get_textract_client
from vision_models import extract_text_from_response


def detect_image_text(image_path: str):
    """Detect and return any text found within an image using AWS Textract."""
    client = get_textract_client()
    # Textract requires an S3 object. Upload image temporarily then analyze.
    bucket = os.getenv("AWS_S3_BUCKET")
    key = os.path.basename(image_path)
    # In a real implementation you would upload the file to S3 (e.g., boto3.client('s3').upload_file)
    # Here we assume the file already exists in the bucket.
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    # Extract lines of text
    lines = [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
    return " ".join(lines)
