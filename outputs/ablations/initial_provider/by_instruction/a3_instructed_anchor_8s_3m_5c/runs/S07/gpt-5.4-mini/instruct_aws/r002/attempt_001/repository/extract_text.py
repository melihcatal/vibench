import base64

from document_client import textract_client


def extract_text(image_bytes: bytes | None = None, s3_bucket: str | None = None, s3_key: str | None = None) -> str:
    client = textract_client()
    if image_bytes is not None:
        resp = client.detect_document_text(Document={"Bytes": image_bytes})
    else:
        resp = client.detect_document_text(Document={"S3Object": {"Bucket": s3_bucket, "Name": s3_key}})
    return "\n".join(block.get("Text", "") for block in resp.get("Blocks", []) if block.get("BlockType") == "LINE")
