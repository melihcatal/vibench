import os
from googletrans import Translator

translator = Translator()

def translate_query(query, dest_lang='en'):
    return translator.translate(query, dest=dest_lang).text
