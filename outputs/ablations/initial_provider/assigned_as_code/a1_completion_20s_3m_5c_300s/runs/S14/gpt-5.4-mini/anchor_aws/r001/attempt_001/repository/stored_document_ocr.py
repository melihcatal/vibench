import boto3

from storage_client import load_storage_config
from storage_models import normalize_object_name


def stored_document_ocr(payload, config=None):
    cfg = load_storage_config(config)
    client = boto3.client("textract", region_name=cfg["region"])
    object_name = normalize_object_name(payload)
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": cfg["bucket"], "Name": object_name}}
    )
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))
    return {"object_name": object_name, "text": "\n".join(lines), "blocks": response.get("Blocks", [])}
