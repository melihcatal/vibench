from document_client import textract_client


def extract_layout(image_bytes: bytes | None = None, s3_bucket: str | None = None, s3_key: str | None = None) -> list[dict]:
    client = textract_client()
    source = {"Bytes": image_bytes} if image_bytes is not None else {"S3Object": {"Bucket": s3_bucket, "Name": s3_key}}
    resp = client.analyze_document(Document=source, FeatureTypes=["LAYOUT"])
    return resp.get("Blocks", [])
