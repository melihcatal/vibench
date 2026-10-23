from typing import Any, Dict, List

import boto3

from storage_client import create_s3_client, get_storage_config


def stored_asset_summary(bucket: str, key: str) -> Dict[str, Any]:
    config = get_storage_config()
    s3_client = create_s3_client(config)
    comprehend = boto3.client("comprehend", region_name=config.aws_region)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    summary = text[:400]
    key_phrases = []
    if text.strip():
        resp = comprehend.detect_key_phrases(Text=text[:4500], LanguageCode="en")
        key_phrases = [p.get("Text") for p in resp.get("KeyPhrases", []) if p.get("Text")]
    return {"bucket": bucket, "key": key, "summary": summary, "key_phrases": key_phrases}
