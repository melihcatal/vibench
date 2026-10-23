from typing import Optional
import boto3
from bs4 import BeautifulSoup
from translation_models import TranslationRequest, TranslationResponse

class MarkupTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def translate_markup(
        self, 
        markup: str, 
        source_lang: str, 
        target_lang: str,
        formality: Optional[str] = None
    ) -> str:
        soup = BeautifulSoup(markup, 'html.parser')
        text_elements = soup.find_all(text=True)
        
        for element in text_elements:
            if element.parent.name in ['script', 'style']:
                continue
            
            if element.strip():
                request = TranslationRequest(
                    text=element,
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
                
                element.replace_with(response['TranslatedText'])
        
        return str(soup)