import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse


# Amazon Translate service – use AWS keys from env
class PlatformOutputLocalization:
    """
    Translate model output into another locale using Amazon Translate.
    Returns the translated text alongside original response metadata.
    """

    def __init__(self):
        import boto3

        self.client = boto3.client("translate")
        self.source_lang = "en"
        self.target_lang = "es"  # change as needed

    def localize(self, response: ModelInvocationResponse) -> dict:
        source_text = response.choices[0]["message"]["content"]
        # Amazon Translate expects a single string; if multiple chunks, join them
        translated = self.client.translate_text(
            Text=source_text,
            SourceLanguageCode=self.source_lang,
            TargetLanguageCode=self.target_lang,
        )
        return {
            "original": source_text,
            "translated": translated.get("TranslatedText", ""),
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
        }
