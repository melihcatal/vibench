import boto3
from translate import Translator


def translate_script(script, target_language="es"):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(script)
    return translation
