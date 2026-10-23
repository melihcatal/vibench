import os
from azure.ai.translation.text import TextTranslationClient

def get_translation_client():
    return TextTranslationClient(endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com", credential=os.getenv('AZURE_TRANSLATOR_KEY'))
