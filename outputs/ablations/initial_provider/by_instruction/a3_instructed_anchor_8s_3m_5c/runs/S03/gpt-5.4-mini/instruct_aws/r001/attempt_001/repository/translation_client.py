import os
from typing import Optional

import boto3


class TranslationClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self.client = boto3.client("translate", region_name=self.region_name)

    def translate_text(self, text: str, source_language_code: str, target_language_code: str) -> str:
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return response.get("TranslatedText", "")

    def batch_translate_text(self, texts, source_language_code: str, target_language_code: str):
        return [self.translate_text(text, source_language_code, target_language_code) for text in texts]


def get_translation_client() -> TranslationClient:
    return TranslationClient()
