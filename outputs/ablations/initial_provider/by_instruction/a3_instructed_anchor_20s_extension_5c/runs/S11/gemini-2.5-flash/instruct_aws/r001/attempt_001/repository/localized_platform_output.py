import boto3
from model_client import get_translate_client

def translate_platform_output(
    text: str,
    source_language_code: str,
    target_language_code: str,
) -> dict:
    """
    Translates platform model output for another locale using AWS Translate.
    """
    client = get_translate_client()

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    return response
