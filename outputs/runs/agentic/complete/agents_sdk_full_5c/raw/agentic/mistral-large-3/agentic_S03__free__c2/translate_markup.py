from typing import Optional
import boto3
from bs4 import BeautifulSoup
from translation_models import TranslationRequest, TranslationResponse

class MarkupTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_markup(self, request: TranslationRequest) -> TranslationResponse:
        soup = BeautifulSoup(request.text, 'html.parser')
        text_elements = soup.find_all(text=True)

        for element in text_elements:
            if element.parent.name not in ['script', 'style'] and element.strip():
                result = self.client.translate_text(
                    Text=str(element),
                    SourceLanguageCode=request.source_lang,
                    TargetLanguageCode=request.target_lang,
                    Settings={
                        'Formality': request.formality.value if request.formality else 'AUTO'
                    }
                )
                element.replace_with(result['TranslatedText'])

        return TranslationResponse(
            translated_text=str(soup),
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )