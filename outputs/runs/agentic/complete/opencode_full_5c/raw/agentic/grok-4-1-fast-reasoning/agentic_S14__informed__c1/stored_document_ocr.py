from storage_client import s3_config
import boto3


def extract_text_from_stored_document(bucket: str, key: str) -> str:
    client = boto3.client("textract", **s3_config)
    resp = client.detect_document_text(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    text = "\n".join(
        block["Text"] for block in resp["Blocks"] if block["BlockType"] == "LINE"
    )
    return text.strip()
