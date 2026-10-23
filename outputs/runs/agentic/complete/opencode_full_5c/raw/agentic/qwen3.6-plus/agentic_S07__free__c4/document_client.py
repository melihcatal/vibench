import os
import base64
from typing import Optional

import boto3
from botocore.config import Config


AWS_TEXTRACT_REGION = os.getenv("AWS_TEXTRACT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_TEXTRACT_ENDPOINT = f"https://textract.{AWS_TEXTRACT_REGION}.amazonaws.com"


def get_textract_client() -> boto3.client:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_TEXTRACT_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=60,
        connect_timeout=10,
    )
    return session.client("textract", config=config)


def get_textract_async_client() -> boto3.client:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_TEXTRACT_REGION,
    )
    config = Config(
        retries={"max_attempts": 5, "mode": "adaptive"},
        read_timeout=120,
        connect_timeout=10,
    )
    return session.client("textract", config=config)


def load_image_as_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def load_image_as_base64(image_path: str) -> str:
    image_bytes = load_image_as_bytes(image_path)
    return base64.b64encode(image_bytes).decode("utf-8")


def build_textract_image_bytes(
    image_path: Optional[str] = None, image_bytes: Optional[bytes] = None
) -> dict:
    if image_path:
        raw_bytes = load_image_as_bytes(image_path)
        return {"Bytes": raw_bytes}
    elif image_bytes:
        return {"Bytes": image_bytes}
    else:
        raise ValueError("Either image_path or image_bytes must be provided")


def normalize_textract_response(response: dict) -> dict:
    blocks = response.get("Blocks", [])
    block_map = {}
    for block in blocks:
        block_id = block.get("Id")
        if block_id:
            block_map[block_id] = block
    return {
        "blocks": blocks,
        "block_map": block_map,
        "document_metadata": response.get("DocumentMetadata", {}),
        "analyze_type": response.get("AnalyzeType", "DOCUMENT"),
        "job_status": response.get("JobStatus", "SUCCEEDED"),
    }
