from typing import Dict, Any
from google.cloud import translate_v2 as translate
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

class DictionaryTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            "credentials.json"
        )

    def translate_dictionary_values(
        self, 
        dictionary: Dict[str, Any],
        target_language: str, 
        source_language: str = None,
        model: str = "nmt"
    ) -> DictionaryTranslationResponse:
        values = [str(v) for v in dictionary.values() if isinstance(v, (str, int, float))]
        results = self.client.translate(
            values,
            target_language=target_language,
            source_language=source_language,
            model=model
        )

        translated_dict = dictionary.copy()
        value_iter = iter(results)
        for key, value in dictionary.items():
            if isinstance(value, (str, int, float)):
                translated_dict[key] = value_iter.__next__()["translatedText"]

        return DictionaryTranslationResponse(
            translated_dictionary=translated_dict,
            detected_source_language=results[0].get("detectedSourceLanguage") if results else None,
            model_used=model
        )

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    translator = DictionaryTranslator()
    return translator.translate_dictionary_values(
        dictionary=request.dictionary,
        target_language=request.target_language,
        source_language=request.source_language
    )