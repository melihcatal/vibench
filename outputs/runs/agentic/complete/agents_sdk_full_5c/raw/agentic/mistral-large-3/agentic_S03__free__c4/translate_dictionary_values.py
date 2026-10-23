from typing import Dict, Any, Optional
import boto3
from translation_models import TranslationRequest, TranslationResponse

class DictionaryTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_dictionary_values(
        self, 
        dictionary: Dict[str, Any], 
        source_lang: str, 
        target_lang: str,
        formality: Optional[str] = None
    ) -> Dict[str, Any]:
        def translate_value(value: Any) -> Any:
            if isinstance(value, str):
                request = TranslationRequest(
                    text=value,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    formality=formality
                )
                
                response = self.client.translate_text(
                    Text=request.text,
                    SourceLanguageCode=request.source_lang,
                    TargetLanguageCode=request.target_lang,
                    Settings={
                        'Formality': request.formality.capitalize() if request.formality else 'Informal'
                    } if request.formality else {}
                )
                
                return response['TranslatedText']
            elif isinstance(value, dict):
                return self.translate_dictionary_values(value, source_lang, target_lang, formality)
            elif isinstance(value, list):
                return [translate_value(item) for item in value]
            else:
                return value
        
        return {key: translate_value(value) for key, value in dictionary.items()}