import os
from azure.cognitiveservices.language.text.translation import TextTranslationClient
from msrest.authentication import CognitiveServicesCredentials

def stored_text_translate(text, target_language):
    subscription_key = os.getenv('TRANSLATOR_SUBSCRIPTION_KEY')
    endpoint = os.getenv('TRANSLATOR_ENDPOINT')
    translator_client = TextTranslationClient(credentials=CognitiveServicesCredentials(subscription_key), endpoint=endpoint)
    result = translator_client.translate(text, target_language)
    print(f'Translated text: {result[0].text}')
    return result[0].text