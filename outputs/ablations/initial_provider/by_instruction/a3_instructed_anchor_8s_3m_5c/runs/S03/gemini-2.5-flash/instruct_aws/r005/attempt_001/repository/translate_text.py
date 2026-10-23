import boto3
import os

def translate_text(text: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates a single text string between languages using AWS Translate.
    """
    client = boto3.client(
        'translate',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )
    
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    
    return response['TranslatedText']
