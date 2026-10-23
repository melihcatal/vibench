import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)
language_translator.set_service_url(os.getenv('WATSONX_URL'))

def appeal_translate(text):
    translation = language_translator.translate(
        text=text,
        model_id='en-es').get_result()
    return translation['translations'][0]['translation']