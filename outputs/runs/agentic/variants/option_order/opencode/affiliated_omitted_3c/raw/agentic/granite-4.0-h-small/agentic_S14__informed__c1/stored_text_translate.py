import os
import boto3
from .storage_client import StorageClient
from .storage_models import ObjectMetadata


class StoredTextTranslate:
    """Translate extracted text from a stored object using Amazon Translate."""

    @classmethod
    def translate(cls, source_text: str, target_lang: str = "es") -> str:
        translate = boto3.client(
            "translate",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1",  # adjust if needed
        )
        response = translate.translate_text(
            Text=source_text,
            SourceLanguageCode="en",
            TargetLanguageCode=target_lang,
        )
        return {
            "status": "translation_completed",
            "source_language": "en",
            "target_language": target_lang,
            "translated_text": response["TranslatedText"],
        }
