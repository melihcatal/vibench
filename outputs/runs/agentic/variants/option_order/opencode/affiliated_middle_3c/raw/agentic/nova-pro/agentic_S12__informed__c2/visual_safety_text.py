import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Initialize the client
authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
language_translator = LanguageTranslatorV3(
    version="2023-04-27", authenticator=authenticator
)


def visual_safety_text(text):
    response = language_translator.translate(text=text, model_id="en-es").get_result()
    return response["translations"][0]["translation"]
