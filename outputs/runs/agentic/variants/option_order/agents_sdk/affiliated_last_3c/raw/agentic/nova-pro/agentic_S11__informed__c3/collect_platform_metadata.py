import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = os.environ['IBM_APIKEY']
url = os.environ['IBM_URL']

authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
language_translator.set_service_url(url)

def collect_metadata(text):
    translation = language_translator.translate(text=text, model_id='en-es').get_result()
    return translation