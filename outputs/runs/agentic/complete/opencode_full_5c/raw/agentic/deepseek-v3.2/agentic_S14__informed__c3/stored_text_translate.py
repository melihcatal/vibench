import boto3
import os
from botocore.exceptions import ClientError


def translate_extracted_text(
    text, source_language_code="auto", target_language_code="en"
):
    """
    Translate text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate
        source_language_code: Source language code (default: 'auto' for auto-detection)
        target_language_code: Target language code (default: 'en' for English)

    Returns:
        dict: Translation results including translated text and language detection
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )

        return {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", source_language_code),
            "target_language": target_language_code,
            "provider": "Amazon Translate",
        }
    except ClientError as e:
        raise Exception(f"Failed to translate text using Amazon Translate: {e}")
