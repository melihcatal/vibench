import os
from deepl import Translator

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
