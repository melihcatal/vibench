from typing import Optional
import boto3
from translation_models import TranslationRequest, TranslationResponse

class TextTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        result = self.client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_lang,
            TargetLanguageCode=request.target_lang,
            Settings={
                'Formality': request.formality.value if request.formality else 'AUTO',
                'Profanity': 'MASK' if request.mask_profanity else 'NO_MASK'
            }
        )
        return TranslationResponse(
            translated_text=result['TranslatedText'],
            source_lang=result.get('SourceLanguageCode', request.source_lang),
            target_lang=result.get('TargetLanguageCode', request.target_lang),
            detected_language_code=result.get('DetectedLanguageCode')
        )