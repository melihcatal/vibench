from typing import Dict, Any
from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(payload: DictionaryTranslationRequest, config: dict) -> DictionaryTranslationResponse:
    client = TranslationClient(project_id=config["project_id"], location=config.get("location", "global"))
    
    values_to_translate = list(payload.data.values())
    translated_values = client.translate_text(
        texts=values_to_translate,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )

    translated_data = {}
    keys = list(payload.data.keys())
    for i, key in enumerate(keys):
        translated_data[key] = translated_values[i]

    return DictionaryTranslationResponse(
        translated_data=translated_data,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
