import os

import boto3

from document_client import load_document_input, s3_object_reference, textract_client


def ocr_embedding(bucket: str | None = None, key: str | None = None):
    bucket, key, version = load_document_input(bucket, key, None)
    text = "\n".join([b.get("Text", "") for b in textract_client().detect_document_text(Document=s3_object_reference(bucket, key, version)).get("Blocks", []) if b.get("BlockType") == "LINE"])
    return boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1").invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":"{text.replace(chr(34), chr(92)+chr(34))}"' + "}").encode("utf-8"), contentType="application/json", accept="application/json")
