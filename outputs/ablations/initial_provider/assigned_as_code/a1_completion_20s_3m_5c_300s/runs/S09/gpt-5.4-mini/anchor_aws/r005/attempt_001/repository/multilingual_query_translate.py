import os

import boto3


def multilingual_query_translate(payload, config=None):
    region = (config or {}).get("region", os.getenv("AWS_REGION", "us-east-1"))
    client = boto3.client("translate", region_name=region)
    response = client.translate_text(Text=payload["query"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload.get("target_language", "en"))
    return {"translated_query": response["TranslatedText"]}
