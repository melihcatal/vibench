import os

import boto3


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region") or os.environ.get("AWS_REGION", "us-east-1"))
    response = client.translate_text(Text=payload["query"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload.get("target_language", "en"))
    return {"translated_query": response["TranslatedText"]}
