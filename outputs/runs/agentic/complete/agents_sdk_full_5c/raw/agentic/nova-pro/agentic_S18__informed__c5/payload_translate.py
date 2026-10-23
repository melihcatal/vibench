import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

# Configuration
endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
key = os.getenv('AZURE_TRANSLATOR_KEY')

# Authenticate
client = TextTranslationClient(endpoint=endpoint, credential=TextTranslationApiKeyCredential(key))

# Translate text
def translate_text(text, to_language):
    result = client.translate(content=[text], to=[to_language])[0]
    return result.translations[0].text