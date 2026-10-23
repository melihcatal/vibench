import os
from typing import Optional

# Amazon Translate integration
import boto3


class TranslationClient:
    """Local helper to configure and expose Amazon Translate."""

    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            "translate",
            region_name=region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def translate_text(
        self, source_text: str, source_lang: str = "en", target_lang: str = "es"
    ) -> str:
        """Translate a single text string."""
        response = self.client.translate_text(
            Text=source_text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang,
        )
        return response["TranslatedText"]


def translate_text(
    source_text: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Public function that translates a single text string using Amazon Translate."""
    client = TranslationClient()
    return client.translate_text(source_text, source_lang, target_lang)
