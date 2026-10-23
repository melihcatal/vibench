from typing import List, Dict, Any
import boto3
from translation_client import AWSTranslateClient
from translation_models import BatchTranslationPayload


def batch_translate(payload: BatchTranslationPayload, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = AWSTranslateClient(region_name=config.get("region", "us-east-1"))
    translated_texts = []

    # AWS Translate does not have a direct synchronous batch translation for a list of strings.
    # The StartTextTranslationJob is asynchronous for documents.
    # For this exercise, we iterate and translate each text individually.
    for text in payload["texts"]:
        response = client.translate_text(
            text=text,
            source_language=payload["source_language"],
            target_language=payload["target_language"],
        )
        translated_texts.append(response["TranslatedText"])

    return {
        "translated_texts": translated_texts,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
