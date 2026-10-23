from dataclasses import dataclass
import os

from google.cloud import translate_v3 as translate

@dataclass
class TranslateDictValuesRequest:
    dictionary: dict[str, str]
    source_language_code: str
    target_language_code: str

@dataclass
class TranslateDictValuesResponse:
    translated_dictionary: dict[str, str]
    detected_language_codes_per_value: dict[str, str]

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_dictionary_values(self, request: TranslateDictValuesRequest) -> TranslateDictValuesResponse:
        original_values = list(request.dictionary.values())
        original_keys = list(request.dictionary.keys())

        if not original_values:
            return TranslateDictValuesResponse(translated_dictionary={}, detected_language_codes_per_value={})

        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=original_values,
                source_language_code=request.source_language_code,
                target_language_code=request.target_language_code,
            )
        )

        translated_dictionary = {}
        detected_language_codes_per_value = {}
        for i, key in enumerate(original_keys):
            translated_dictionary[key] = response.translations[i].translated_text
            detected_language_codes_per_value[key] = response.translations[i].detected_language_code

        return TranslateDictValuesResponse(
            translated_dictionary=translated_dictionary,
            detected_language_codes_per_value=detected_language_codes_per_value
        )
