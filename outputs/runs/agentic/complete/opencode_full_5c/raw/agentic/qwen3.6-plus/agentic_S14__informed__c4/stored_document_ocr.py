import os
import base64
from typing import Optional, List, Dict, Any

import boto3

from storage_client import get_bucket_name


def stored_document_ocr(
    object_key: str,
    bucket: Optional[str] = None,
    feature_types: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if bucket is None:
        bucket = get_bucket_name()

    if feature_types is None:
        feature_types = ["TABLES", "FORMS", "SIGNATURES"]

    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    textract_client = boto3.client(
        "textract",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    s3_object = {
        "Bucket": bucket,
        "Name": object_key,
    }

    try:
        response = textract_client.analyze_document(
            Document={"S3Object": s3_object},
            FeatureTypes=feature_types,
        )

        blocks = response.get("Blocks", [])
        text_lines = []
        tables = []
        forms = []
        key_value_map = {}

        for block in blocks:
            block_type = block.get("BlockType")
            if block_type == "LINE":
                text_lines.append(block.get("Text", ""))
            elif block_type == "TABLE":
                tables.append(block)
            elif block_type == "KEY_VALUE_SET":
                entity_types = block.get("EntityTypes", [])
                if "KEY" in entity_types:
                    key_text = block.get("Text", "")
                    forms.append(
                        {"key": key_text, "value": None, "block_id": block["Id"]}
                    )
                    key_value_map[block["Id"]] = key_text
                elif "VALUE" in entity_types:
                    value_text = block.get("Text", "")
                    forms.append(
                        {"key": None, "value": value_text, "block_id": block["Id"]}
                    )

        full_text = "\n".join(text_lines)

        return {
            "success": True,
            "object_key": object_key,
            "bucket": bucket,
            "full_text": full_text,
            "lines": text_lines,
            "tables": tables,
            "forms": forms,
            "block_count": len(blocks),
            "detect_document_type": response.get("DetectDocumentType", False),
        }
    except Exception as exc:
        return {
            "success": False,
            "object_key": object_key,
            "bucket": bucket,
            "error": str(exc),
        }
