import os
from deepl import Translator

deepl_auth_key = os.getenv('DEEPL_AUTH_KEY')

translator = Translator(deepl_auth_key)