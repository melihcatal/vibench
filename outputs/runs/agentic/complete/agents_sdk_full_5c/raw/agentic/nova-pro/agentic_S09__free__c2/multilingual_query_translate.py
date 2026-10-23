from googletrans import Translator

translator = Translator()

def translate_query(query, src_lang, dest_lang):
    translated = translator.translate(query, src=src_lang, dest=dest_lang)
    return translated.text