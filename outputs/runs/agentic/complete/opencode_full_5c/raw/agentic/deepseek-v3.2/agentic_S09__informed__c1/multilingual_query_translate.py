import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def multilingual_query_translate(
    query: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """Translate queries before multilingual embedding search using Amazon Translate."""
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        translate_args = {
            "Text": query,
            "SourceLanguageCode": source_language or "auto",
            "TargetLanguageCode": target_language,
        }

        response = client.translate_text(**translate_args)

        return response["TranslatedText"]

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "UnsupportedLanguagePairException":
            # Fallback: return original query if translation not supported
            print(
                f"Warning: Translation from {source_language or 'auto'} to {target_language} not supported"
            )
            return query
        else:
            raise Exception(f"Amazon Translate error: {str(e)}")
