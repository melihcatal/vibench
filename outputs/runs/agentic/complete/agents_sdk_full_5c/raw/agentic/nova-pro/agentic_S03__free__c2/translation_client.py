import os
from deepl import Translator

def get_translator():
    auth_key = os.getenv('DEEPL_API_KEY')
    return Translator(auth_key)