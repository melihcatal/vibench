import os
from typing import Dict, Any
import boto3
from security_models import TranslationResult


class ComplianceNoteTranslator:
    def __init__(self):
        self.translate_client = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def translate_compliance_note(
        self, text: str, source_language: str = "en", target_language: str = "es"
    ) -> TranslationResult:
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )

            return TranslationResult(
                translated_text=response["TranslatedText"],
                source_language=response["SourceLanguageCode"],
                target_language=response["TargetLanguageCode"],
            )
        except Exception as e:
            raise Exception(f"Failed to translate compliance note: {e}")
