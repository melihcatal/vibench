import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

class TranslatorClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
        self.key = os.getenv('AZURE_TRANSLATOR_KEY')
        self.client = TextTranslationClient(endpoint=self.endpoint, credential=TextTranslationApiKeyCredential(self.key))
    
    def translate(self, text, to_language='en'):
        result = self.client.translate([text], to_language)
        return result[0].translations[0].text

translator = TranslatorClient()

def translate_query(query, to_language='en'):
    return translator.translate(query, to_language)