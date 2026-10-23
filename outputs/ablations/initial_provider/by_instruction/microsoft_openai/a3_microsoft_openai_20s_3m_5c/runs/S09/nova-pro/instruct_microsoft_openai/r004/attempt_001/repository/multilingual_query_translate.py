from googletrans import Translator

def multilingual_query_translate(query: str, target_language: str):
    translator = Translator()
    translation = translator.translate(query, dest=target_language)
    return translation.text