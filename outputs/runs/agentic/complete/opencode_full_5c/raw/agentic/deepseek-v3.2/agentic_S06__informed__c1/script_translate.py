import os
import boto3
from botocore.exceptions import ClientError


def translate_text(text, source_language_code="en", target_language_code="es"):
    """Translate narration scripts before synthesis using Amazon Translate."""
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return response["TranslatedText"]
    except ClientError as e:
        raise Exception(f"Translation failed: {e}")


def translate_batch(texts, source_language_code="en", target_language_code="es"):
    """Translate multiple texts in batch."""
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    results = []
    for text in texts:
        try:
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
            )
            results.append(response["TranslatedText"])
        except ClientError as e:
            results.append(f"Error: {str(e)}")

    return results
