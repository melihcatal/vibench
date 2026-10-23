import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
key = os.getenv('AZURE_TRANSLATOR_KEY')

translation_client = TextTranslationClient(endpoint=endpoint, credential=TranslatorCredential(key))

documents = ["This is a log message to translate."]
response = translation_client.translate(documents, 'en', 'es')
for translated_document in response:
    print(translated_document.translations[0].text)