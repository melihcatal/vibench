from __future__ import annotations

from typing import Dict

import boto3

from storage_client import load_storage_config


def translate_stored_text(bucket: str, key: str, target_language: str = "en") -> Dict[str, str]:
    load_storage_config(bucket)
    textract = boto3.session.Session().client("textract")
    translate = boto3.session.Session().client("translate")
    detected = textract.detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
    source_text = "\n".join(
        block["Text"] for block in detected.get("Blocks", []) if block.get("BlockType") == "LINE" and block.get("Text")
    )
    translation = translate.translate_text(Text=source_text or "", SourceLanguageCode="auto", TargetLanguageCode=target_language)
    return {
        "bucket": bucket,
        "key": key,
        "source_text": source_text,
        "translated_text": translation.get("TranslatedText", ""),
        "source_language": translation.get("SourceLanguageCode", "auto"),
        "target_language": target_language,
    }
