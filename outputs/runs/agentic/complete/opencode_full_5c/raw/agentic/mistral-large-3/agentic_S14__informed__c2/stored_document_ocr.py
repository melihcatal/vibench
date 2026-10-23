import os
from typing import Dict
from boto3 import client
from botocore.exceptions import ClientError


def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
) -> Dict:
    """
    Runs OCR on a document stored in Amazon S3 using Amazon Textract.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the document in the bucket.

    Returns:
        Dictionary containing OCR results (e.g., text, blocks, detected languages).

    Raises:
        ClientError: If the OCR process fails.
    """
    textract_client = client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": object_key,
                }
            }
        )

        return {
            "text": " ".join(
                [
                    item["Text"]
                    for item in response.get("Blocks", [])
                    if item["BlockType"] == "LINE"
                ]
            ),
            "blocks": response.get("Blocks", []),
        }
    except ClientError as e:
        raise Exception(f"Failed to run OCR: {e}")
