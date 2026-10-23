import boto3
from typing import Dict, Any
from safety_client import get_aws_client
from safety_models import TranslationRequest, TranslationResult

def appeal_translate(payload: TranslationRequest, config: Dict[str, Any] = None) -> TranslationResult:
    config = config or {}
    client = get_aws_client("translate", config)

    response = client.translate_text(
        Text=payload.text_to_translate,
        SourceLanguageCode=payload.source_language,
        TargetLanguageCode=payload.target_language
    )

    return TranslationResult(translated_text=response["TranslatedText"])
