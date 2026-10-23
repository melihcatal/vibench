import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

api_key = os.getenv("IBM_TRANSLATOR_APIKEY")
url = os.getenv("IBM_TRANSLATOR_URL")
version = "2018-05-01"

authenticator = IAMAuthenticator(api_key)
language_translator = LanguageTranslatorV3(version=version, authenticator=authenticator)
language_translator.set_service_url(url)


def translate_text(text, target_language="es"):
    translation = language_translator.translate(
        text=text, model_id="en-es"
    ).get_result()
    return translation["translations"][0]["translation"]
