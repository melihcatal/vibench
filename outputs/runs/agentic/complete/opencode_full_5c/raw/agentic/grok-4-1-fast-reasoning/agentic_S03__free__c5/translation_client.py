import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise ValueError("DEEPL_AUTH_KEY environment variable is required.")

translator = Translator(DEEPL_AUTH_KEY)
