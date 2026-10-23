import os

from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def translate_appeal(text):
    apikey = os.getenv("IBM_TRANSLATE_APIKEY")
    url = os.getenv("IBM_TRANSLATE_URL")

    authenticator = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version="2018-05-01", authenticator=authenticator
    )
    language_translator.set_service_url(url)

    translation = language_translator.translate(
        text=text, model_id="en-es"
    ).get_result()
    return translation["translations"][0]["translation"]
