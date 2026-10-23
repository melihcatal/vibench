import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=authenticator
)


def check_safety(text):
    response = language_translator.translate(text=text, model_id="en-es").get_result()
    return response["translations"][0]["translation"]
