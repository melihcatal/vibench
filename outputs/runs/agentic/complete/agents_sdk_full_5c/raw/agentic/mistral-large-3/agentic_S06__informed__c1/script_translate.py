import os
from typing import Dict
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def translate_script(
    text: str,
    source_language: str,
    target_language: str
) -> str:
    """
    Translate narration scripts using Amazon Translate.
    """
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    
    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response["TranslatedText"]
    except (BotoCoreError, ClientError) as e:
        raise Exception(f"Failed to translate text: {e}")