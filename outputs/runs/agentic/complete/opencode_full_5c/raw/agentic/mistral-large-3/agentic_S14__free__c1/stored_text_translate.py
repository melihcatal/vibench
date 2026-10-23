from typing import Dict
import requests
from storage_client import StorageClient


def stored_text_translate(
    bucket_name: str, object_key: str, target_language: str = "es"
) -> str:
    """
    Translates text extracted from a document stored in Amazon S3 using AWS Translate.
    """
    client = StorageClient().get_client()

    try:
        # Fetch the object from S3
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        text = response["Body"].read().decode("utf-8")

        # Call AWS Translate
        translate_client = client("translate", region_name="us-east-1")
        translate_response = translate_client.translate_text(
            Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
        )

        return translate_response["TranslatedText"]
    except Exception as e:
        raise Exception(f"Failed to translate text from S3 document: {str(e)}")
