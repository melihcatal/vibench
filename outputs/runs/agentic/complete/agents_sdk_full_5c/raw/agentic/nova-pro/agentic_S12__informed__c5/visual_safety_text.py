from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def check_text_safety(text):
    authenticator = IAMAuthenticator('your-api-key')
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )
    language_translator.set_service_url('your-service-url')
    translation = language_translator.translate(
        text=text,
        model_id='en-es'
    ).get_result()
    return translation