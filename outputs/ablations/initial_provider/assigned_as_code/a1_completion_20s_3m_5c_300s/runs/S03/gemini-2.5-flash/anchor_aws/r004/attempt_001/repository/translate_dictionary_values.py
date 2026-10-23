from typing import Dict, Any
import boto3
from translation_client import get_translate_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(payload: DictionaryTranslationRequest, config: dict = None) -> DictionaryTranslationResponse:
    config = config or {}
    client = get_translate_client(config.get("region", "us-east-1"))

    translated_data: Dict[str, str] = {}
    for key, value in payload.data.items():
        response = client.translate_text(
            Text=value,
            SourceLanguageCode=payload.source_language,
            TargetLanguageCode=payload.target_language,
        )
        translated_data[key] = response["TranslatedText"]
    
    return DictionaryTranslationResponse(
        data=translated_data,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
