import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def quality_summary(text):
    api_key = os.getenv("WATSONX_API_KEY")
    url = os.getenv("WATSONX_URL")
    authenticator = IAMAuthenticator(api_key)
    language_translator = LanguageTranslatorV3(
        version="2018-05-01", authenticator=authenticator
    )
    language_translator.set_service_url(url)
    translation = language_translator.translate(
        text=text, model_id="en-es"
    ).get_result()
    return translation
