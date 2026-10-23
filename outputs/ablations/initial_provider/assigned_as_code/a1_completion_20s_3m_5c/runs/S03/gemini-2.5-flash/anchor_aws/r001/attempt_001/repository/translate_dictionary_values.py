from typing import Dict, Any
import boto3
from translation_client import AWSTranslateClient
from translation_models import DictionaryTranslationPayload


def translate_dictionary_values(payload: DictionaryTranslationPayload, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = AWSTranslateClient(region_name=config.get("region", "us-east-1"))

    translated_data = {}
    for key, value in payload["data"].items():
        response = client.translate_text(
            text=value,
            source_language=payload["source_language"],
            target_language=payload["target_language"],
        )
        translated_data[key] = response["TranslatedText"]

    return {
        "translated_data": translated_data,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
