import os
from typing import Dict

import boto3
from botocore.exceptions import ClientError


class AmazonTranslateClient:
    def __init__(self):
        self.translate_client = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def translate_text(
        self, text: str, source_language: str = "auto", target_language: str = "en"
    ) -> Dict:
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
            return {
                "translated_text": response.get("TranslatedText"),
                "source_language": response.get("SourceLanguageCode"),
            }
        except ClientError as e:
            raise Exception(f"Failed to translate text: {e}")
