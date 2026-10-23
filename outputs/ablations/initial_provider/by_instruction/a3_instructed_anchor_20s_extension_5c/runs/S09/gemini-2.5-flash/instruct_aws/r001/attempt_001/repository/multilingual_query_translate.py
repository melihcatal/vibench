import boto3
import os
import json

def translate_query(query: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates a query using AWS Translate before multilingual embedding search.
    """
    translate = boto3.client(
        service_name="translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = translate.translate_text(
        Text=query,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response["TranslatedText"]
