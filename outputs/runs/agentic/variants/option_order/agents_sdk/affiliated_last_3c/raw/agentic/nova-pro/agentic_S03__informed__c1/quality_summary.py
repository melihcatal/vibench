import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

os.environ['IBM_API_KEY_ID'] = 'your-ibm-api-key'

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

url = 'https://api.us-south.language-translator.watson.cloud.ibm.com/instances/your-instance-id'
language_translator.set_service_url(url)

def summarize_quality_issues(text, translation):
    response = language_translator.identify(text).get_result()
    return response