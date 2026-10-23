import os
import boto3

def translate_text(text: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates text extracted from a stored document using Amazon Translate.

    Args:
        text (str): The text to translate.
        source_language_code (str): The language code of the input text (e.g., 'en', 'es').
        target_language_code (str): The language code to translate the text into (e.g., 'fr', 'de').

    Returns:
        str: The translated text.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables.")

    translate_client = boto3.client(
        "translate",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']
