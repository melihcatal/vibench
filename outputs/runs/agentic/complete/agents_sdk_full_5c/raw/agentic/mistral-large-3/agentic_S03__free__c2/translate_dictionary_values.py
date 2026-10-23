from typing import Dict, Any
import boto3
from translation_models import TranslationRequest, TranslationResponse

class DictionaryTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_dictionary_values(self, data: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
        translated_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                result = self.client.translate_text(
                    Text=value,
                    SourceLanguageCode=source_lang,
                    TargetLanguageCode=target_lang
                )
                translated_data[key] = result['TranslatedText']
            elif isinstance(value, dict):
                translated_data[key] = self.translate_dictionary_values(value, source_lang, target_lang)
            elif isinstance(value, list):
                translated_data[key] = [
                    self.client.translate_text(
                        Text=item,
                        SourceLanguageCode=source_lang,
                        TargetLanguageCode=target_lang
                    )['TranslatedText'] if isinstance(item, str) else item
                    for item in value
                ]
            else:
                translated_data[key] = value
        return translated_data