import os
from deep_translator import GoogleTranslator


def translate_query(query: str, target_language: str = 'en') -> str:
    return GoogleTranslator(source='auto', target=target_language).translate(query)
