import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def archive_summary(transcript):
    apikey = os.environ.get('IBM_LT_APIKEY')
    url = os.environ.get('IBM_LT_URL')
    authenticator = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator
    )
    language_translator.set_service_url(url)
    translation = language_translator.translate(
        text=transcript,
        model_id='en-es'
    ).get_result()
    return translation['translations'][0]['translation']