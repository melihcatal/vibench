import boto3
import os
import json
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def run_ocr_on_stored_document(
    bucket_name: str, object_key: str, textract_client=None
) -> dict:
    """
    Run Amazon Textract OCR on a stored document object.

    Args:
        bucket_name: S3 bucket name containing the document
        object_key: Object key of the document
        textract_client: Optional Textract client (will create if not provided)

    Returns:
        Dictionary with OCR results including extracted text and layout
    """
    # Create Textract client if not provided
    if textract_client is None:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS credentials not found in environment. "
                "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )

        textract_client = boto3.client(
            "textract",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    try:
        # Call Textract to analyze document
        response = textract_client.analyze_document(
            Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
            FeatureTypes=["TABLES", "FORMS", "LAYOUT"],
        )

        # Extract text blocks
        text_blocks = []
        for block in response.get("Blocks", []):
            if block["BlockType"] in ["LINE", "WORD"]:
                text_blocks.append(
                    {
                        "type": block["BlockType"],
                        "text": block.get("Text", ""),
                        "confidence": block.get("Confidence", 0),
                        "geometry": block.get("Geometry", {}),
                    }
                )

        # Extract tables
        tables = []
        for block in response.get("Blocks", []):
            if block["BlockType"] == "TABLE":
                table_data = {
                    "id": block.get("Id", ""),
                    "confidence": block.get("Confidence", 0),
                    "geometry": block.get("Geometry", {}),
                    "relationships": block.get("Relationships", []),
                }
                tables.append(table_data)

        # Extract forms (key-value pairs)
        forms = []
        for block in response.get("Blocks", []):
            if block["BlockType"] == "KEY_VALUE_SET":
                entity_type = block.get("EntityTypes", [])
                if "KEY" in entity_type or "VALUE" in entity_type:
                    form_data = {
                        "id": block.get("Id", ""),
                        "entity_type": entity_type,
                        "confidence": block.get("Confidence", 0),
                        "geometry": block.get("Geometry", {}),
                    }
                    forms.append(form_data)

        # Combine all text
        full_text = " ".join(
            [block["text"] for block in text_blocks if block["type"] == "LINE"]
        )

        return {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "text_blocks": text_blocks,
            "tables": tables,
            "forms": forms,
            "full_text": full_text,
            "block_count": len(response.get("Blocks", [])),
            "document_metadata": response.get("DocumentMetadata", {}),
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        return {
            "success": False,
            "error": str(e),
            "error_code": error_code,
            "bucket": bucket_name,
            "key": object_key,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "bucket": bucket_name,
            "key": object_key,
        }
