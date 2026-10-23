from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('WATSONX_API_KEY')
language_translator = LanguageTranslatorV3(
    version='2023-11-01',
    authenticator=authenticator
)

def moderate_text(text):
    translation = language_translator.translate(
        text=text,
        model_id='en-es'
    ).get_result()
    return translation['translations'][0]['translation']
