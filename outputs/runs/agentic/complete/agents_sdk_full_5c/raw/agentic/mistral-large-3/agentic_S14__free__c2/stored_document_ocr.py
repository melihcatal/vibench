import os
from typing import Optional
import boto3
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def run_ocr_on_stored_document(
    object_key: str,
    output_object_key: Optional[str] = None
) -> str:
    """
    Runs OCR on a stored document in AWS S3 using AWS Textract.
    Returns the extracted text.
    """
    s3_client = get_storage_client()
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "default-bucket")
    output_key = output_object_key or f"ocr-output/{object_key}.txt"

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": object_key
            }
        }
    )

    extracted_text = "\n".join(
        [item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"]
    )

    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=extracted_text.encode("utf-8")
    )

    return extracted_text