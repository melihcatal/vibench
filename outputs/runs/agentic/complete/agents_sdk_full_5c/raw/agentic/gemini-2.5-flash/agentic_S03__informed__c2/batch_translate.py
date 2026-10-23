import deepl
import os
from typing import List, Optional
from translation_client import get_deepl_client

def batch_translate_texts(texts: List[str], target_lang: str, source_lang: Optional[str] = None) -> List[str]:
    """
    Translates a list of text strings while preserving order using DeepL.
    """
    client = get_deepl_client()
    results = client.translate_text(
        texts,
        target_lang=target_lang,
        source_lang=source_lang
    )
    return [result.text for result in results]

if __name__ == '__main__':
    # Example usage (ensure DEEPL_AUTH_KEY is set in environment variables)
    texts_to_translate = ["Hello, world!", "How are you?"]
    target_language = "es"
    translated_texts = batch_translate_texts(texts_to_translate, target_language)
    print(f"Original: {texts_to_translate}")
    print(f"Translated ({target_language}): {translated_texts}")
