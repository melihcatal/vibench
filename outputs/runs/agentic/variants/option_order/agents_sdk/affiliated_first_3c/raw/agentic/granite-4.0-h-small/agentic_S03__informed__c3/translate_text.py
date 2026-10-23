import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(input_text: str, source_lang: str = 'en', target_lang: str = 'fr') -> str:
    """Translate a single text string between languages using the configured provider.
    Uses IBM Watson Language Translator as the concrete provider.
    The provider is identified by the model_id 'en-fr' and is configured via environment variable WATSONX_API_KEY.
    """
    client = get_translation_client()
    request = TranslationRequest(text=input_text, source=source_lang, target=target_lang)
    response = client.translate(request)
    return response.translated_text

if __name__ == '__main__':
    text = 'Hello, world!'
    translated = translate_text(text, source_lang='en', target_lang='fr')
    print(f'Translated: {translated}')
