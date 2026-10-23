import os
from typing import List
from translation_client import TranslationClient

def batch_translate(texts: List[str], source_lang: str = 'en', target_lang: str = 'es') -> List[str]:
    """Translate a list of strings while preserving order using a single request to the provider.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    client = TranslationClient()
    # The provider supports batch translation in a single call
    response = client.batch_translate(texts, source_lang, target_lang)
    # Response is a JSON list of translations in the same order as the input
    translations = json.loads(response)
    return [item['translations'][0]['text'] for item in translations]

if __name__ == '__main__':
    sample_texts = ['Hello', 'How are you?', 'Goodbye']
    print('Original:', sample_texts)
    print('Translated:', batch_translate(sample_texts))