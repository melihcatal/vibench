import os
from deepl import Translator

os.environ["DEEPL_AUTH_KEY"] = "your-api-key"
translator = Translator(os.environ["DEEPL_AUTH_KEY"])
