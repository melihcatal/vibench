import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

def summarize_image(description):
    response = language_translator.translate(
        text=description,
        model_id='en-es'
    ).get_result()
    return response['translations'][0]['translation']