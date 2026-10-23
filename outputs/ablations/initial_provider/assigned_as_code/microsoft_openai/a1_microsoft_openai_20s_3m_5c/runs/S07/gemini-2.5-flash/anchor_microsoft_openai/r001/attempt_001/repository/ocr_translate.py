from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

def ocr_translate(text: str, target_language: str, config=None):
    config = config or {}
    # Endpoint for Azure Translator should be like "https://api.cognitive.microsofttranslator.com/"
    # A sample key can be found in your Azure Translator resource.
    client = TextTranslationClient(
        endpoint=config['translator_endpoint'],
        credential=TranslatorCredential(config['translator_api_key'], config['translator_region'])
    )
    
    result = client.translate(content=[InputTextItem(text=text)], to=[target_language])
    if result and result[0].translations:
        return {'translated_text': result[0].translations[0].text}
    return {'translated_text': text}
