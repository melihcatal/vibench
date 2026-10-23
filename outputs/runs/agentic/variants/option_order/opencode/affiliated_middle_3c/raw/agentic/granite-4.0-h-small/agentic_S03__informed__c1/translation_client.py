import os
import boto3
from typing import Optional

# Amazon Translate integration


class TranslationClient:
    """Local helper to configure and expose Amazon Translate.

    Configuration is read from environment variables for credentials and region.
    """

    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            "translate",
            region_name=region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def translate_text(
        self, source_text: str, source_lang: str = "en", target_lang: str = "es"
    ) -> dict:
        """Call the Amazon Translate API and return the raw response.

        Returns the full API response (including TranslatedText, SourceLanguageCode, etc.).
        """
        return self.client.translate_text(
            Text=source_text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang,
        )
