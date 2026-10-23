import boto3
import os

def translate_consent_text(text: str, source_language_code: str, target_language_code: str) -> str:
    client = boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return response["TranslatedText"]
    except Exception as e:
        raise RuntimeError(f"Error translating consent text with AWS Translate: {e}")
