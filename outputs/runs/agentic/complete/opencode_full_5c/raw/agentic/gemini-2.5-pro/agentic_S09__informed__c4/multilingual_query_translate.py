import boto3
import os


def translate_query(query: str, source_lang: str, target_lang: str) -> str:
    """
    Translates a query to a target language for multilingual embedding search using Amazon Translate.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    response = translate_client.translate_text(
        Text=query, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )

    return response["TranslatedText"]
