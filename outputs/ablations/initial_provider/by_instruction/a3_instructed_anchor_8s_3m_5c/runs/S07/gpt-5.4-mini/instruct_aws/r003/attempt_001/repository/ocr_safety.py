import os

from document_client import load_document_input, s3_object_reference, textract_client


def ocr_safety(bucket: str | None = None, key: str | None = None):
    bucket, key, version = load_document_input(bucket, key, None)
    blocks = textract_client().detect_document_text(Document=s3_object_reference(bucket, key, version)).get("Blocks", [])
    text = "\n".join([b.get("Text", "") for b in blocks if b.get("BlockType") == "LINE"])
    client = __import__("boto3").client("comprehend", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    return client.detect_dominant_language(Text=text), client.detect_key_phrases(Text=text)
