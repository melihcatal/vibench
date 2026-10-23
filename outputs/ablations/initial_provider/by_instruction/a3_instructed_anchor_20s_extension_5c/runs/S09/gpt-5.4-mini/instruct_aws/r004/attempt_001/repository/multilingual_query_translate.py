import os

import boto3


def multilingual_query_translate(query, target_language="en"):
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
    result = client.translate_text(Text=query, SourceLanguageCode="auto", TargetLanguageCode=target_language)
    return {"provider": "aws_translate", "translated_text": result["TranslatedText"], "target_language": target_language}
