import os
from typing import List
from translation_client import get_translation_client, TranslationRequest, TranslationResponse
from translation_models import normalize_batch_request

def batch_translate(texts: List[str], source_lang: str = 'en', target_lang: str = 'fr') -> List[str]:
    """Translate a list of strings while preserving input order.
    Uses IBM Watson Language Translator as the concrete provider.
    The provider is identified by the model_id (e.g., 'en-fr') and configured via WATSONX_API_KEY.
    Batch translation is performed by grouping texts up to the provider's max segment length.
    """
    client = get_translation_client()
    batch_req = normalize_batch_request(texts, source_lang, target_lang)
    responses = client.translate_batch(batch_req)
    # responses is a list of TranslationResponse objects in same order as input
    return [resp.translated_text for resp in responses]

if __name__ == '__main__':
    sample_texts = [
        'The quick brown fox jumps over the lazy dog.',
        'Hello, world!',
        'OpenAI creates powerful language models.'
    ]
    translated = batch_translate(sample_texts, source_lang='en', target_lang='de')
    for original, trans in zip(sample_texts, translated):
        print(f'orig: {original}\n--> de: {trans}\n')
