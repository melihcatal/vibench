import os

import boto3

from document_client import load_document_input, s3_object_reference, textract_client


def ocr_translate(bucket: str | None = None, key: str | None = None, source_language: str = "auto", target_language: str = "en"):
    bucket, key, version = load_document_input(bucket, key, None)
    textract = textract_client()
    text = "\n".join([b.get("Text", "") for b in textract.detect_document_text(Document=s3_object_reference(bucket, key, version)).get("Blocks", []) if b.get("BlockType") == "LINE"])
    return boto3.client("translate", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1").translate_text(Text=text, SourceLanguageCode=source_language if source_language != "auto" else "auto", TargetLanguageCode=target_language)
