import os

import boto3

from document_client import load_document_input, s3_object_reference, textract_client


def document_field_extraction(bucket: str | None = None, key: str | None = None):
    bucket, key, version = load_document_input(bucket, key, None)
    textract = textract_client()
    blocks = textract.analyze_document(Document=s3_object_reference(bucket, key, version), FeatureTypes=["FORMS"]).get("Blocks", [])
    text = "\n".join([b.get("Text", "") for b in blocks if b.get("BlockType") == "LINE"])
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    return client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=text.encode("utf-8"), contentType="text/plain", accept="text/plain")
