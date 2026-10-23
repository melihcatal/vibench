from typing import Any, Dict

import boto3

from storage_client import create_s3_client, get_storage_config


def stored_text_translate(bucket: str, key: str, target_language_code: str = "en") -> Dict[str, Any]:
    config = get_storage_config()
    s3_client = create_s3_client(config)
    translate = boto3.client("translate", region_name=config.aws_region)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    source_text = obj["Body"].read().decode("utf-8", errors="ignore")
    response = translate.translate_text(
        Text=source_text,
        SourceLanguageCode="auto",
        TargetLanguageCode=target_language_code,
    )
    return {
        "bucket": bucket,
        "key": key,
        "source_text": source_text,
        "translated_text": response.get("TranslatedText", ""),
        "source_language_code": response.get("SourceLanguageCode"),
        "target_language_code": response.get("TargetLanguageCode", target_language_code),
    }
