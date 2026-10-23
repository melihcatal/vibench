from typing import Optional
import boto3
from translation_models import TranslationRequest, TranslationResponse

class TextTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_text(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str, 
        formality: Optional[str] = None
    ) -> TranslationResponse:
        request = TranslationRequest(
            text=text, 
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
        
        return TranslationResponse(
            translated_text=response['TranslatedText'],
            source_lang=response['SourceLanguageCode'],
            target_lang=response['TargetLanguageCode'],
            detected_language_code=response.get('DetectedLanguageCode')
        )