import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

translation_client = TextTranslationClient(endpoint=f'https://{os.environ.get('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com', credential=TranslatorCredential(os.environ.get('AZURE_TRANSLATOR_KEY')))

def translate_transcript(text, target_language='es'):
    result = translation_client.translate(text, to=[target_language])
    return result[0].translations[0].text