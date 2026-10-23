import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = os.environ["IBM_API_KEY_ID"]
url = os.environ["IBM_URL"]

authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=authenticator
)

language_translator.set_service_url(url)


def translate_text(text, model_id="en-es"):
    translation = language_translator.translate(
        text=text, model_id=model_id
    ).get_result()
    return translation["translations"][0]["translation"]
