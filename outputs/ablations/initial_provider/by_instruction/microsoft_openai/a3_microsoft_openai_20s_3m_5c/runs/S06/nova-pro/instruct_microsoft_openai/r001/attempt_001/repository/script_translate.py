import os
from azure.cognitiveservices.translation.text import TextTranslationClient, TranslatorTextApiCredentials

def translate_script(script: str, target_language: str) -> str:
    subscription_key = os.getenv('AZURE_TRANSLATOR_KEY')
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    credentials = TranslatorTextApiCredentials(subscription_key)
    client = TextTranslationClient(credentials, endpoint)
    translations = client.translate([script], target_language)
    return translations[0].text