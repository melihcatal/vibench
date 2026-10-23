from typing import List
import boto3
from translation_client import get_translate_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(payload: BatchTranslationRequest, config: dict = None) -> BatchTranslationResponse:
    config = config or {}
    client = get_translate_client(config.get("region", "us-east-1"))

    translated_texts: List[str] = []
    for text_to_translate in payload.texts:
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=payload.source_language,
            TargetLanguageCode=payload.target_language,
        )
        translated_texts.append(response["TranslatedText"])
    
    return BatchTranslationResponse(
        texts=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
