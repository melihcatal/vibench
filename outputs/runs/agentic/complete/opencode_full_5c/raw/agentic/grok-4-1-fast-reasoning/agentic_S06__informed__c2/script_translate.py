import os
import boto3


def translate_script(
    script: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    result = client.translate_text(
        Text=script, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
    )
    return result["TranslatedText"]
