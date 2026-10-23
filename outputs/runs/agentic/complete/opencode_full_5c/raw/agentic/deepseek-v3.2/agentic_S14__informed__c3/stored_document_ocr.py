import boto3
import os
import json
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def run_ocr_on_stored_document(bucket_name, object_key):
    """
    Run OCR on a stored document object using Amazon Textract.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: Object key (path) of the document in S3

    Returns:
        dict: OCR results including extracted text, lines, and confidence scores
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    textract_client = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
        )

        extracted_text = []
        lines = []

        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                line_text = block.get("Text", "")
                confidence = block.get("Confidence", 0)
                geometry = block.get("Geometry", {})

                lines.append(
                    {
                        "text": line_text,
                        "confidence": confidence,
                        "bounding_box": geometry.get("BoundingBox", {}),
                        "provider": "Amazon Textract",
                    }
                )
                extracted_text.append(line_text)

        return {
            "bucket": bucket_name,
            "key": object_key,
            "full_text": " ".join(extracted_text),
            "lines": lines,
            "line_count": len(lines),
            "provider": "Amazon Textract",
        }
    except ClientError as e:
        raise Exception(f"Failed to run OCR using Amazon Textract: {e}")
