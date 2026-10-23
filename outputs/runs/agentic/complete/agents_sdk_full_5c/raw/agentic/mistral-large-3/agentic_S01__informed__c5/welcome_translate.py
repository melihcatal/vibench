import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from typing import List

def translate_welcome_message(text: str, to_languages: List[str]) -> dict:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    endpoint = f"https://api.cognitive.microsofttranslator.com"
    
    credential = TranslatorCredential(key, region)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)
    
    input_text = [InputTextItem(text=text)]
    response = client.translate(content=input_text, to=to_languages)
    
    return {translation.to: translation.text for translation in response[0].translations}