from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from storage_models import StoredTextTranslateResult

TRANSLATE_MODEL = "amazon-translate"


def translate_extracted_text(text: str, target_language: str, source_language: Optional[str] = None) -> StoredTextTranslateResult:
    client = boto3.client("translate")
    try:
        kwargs = {"Text": text, "TargetLanguageCode": target_language}
        if source_language:
            kwargs["SourceLanguageCode"] = source_language
        response = client.translate_text(**kwargs)
        return StoredTextTranslateResult(source_language=response.get("SourceLanguageCode", source_language), target_language=response.get("TargetLanguageCode", target_language), translated_text=response.get("TranslatedText", ""))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"translation failed using {TRANSLATE_MODEL}: {exc}") from exc


__all__ = ["translate_extracted_text"]
