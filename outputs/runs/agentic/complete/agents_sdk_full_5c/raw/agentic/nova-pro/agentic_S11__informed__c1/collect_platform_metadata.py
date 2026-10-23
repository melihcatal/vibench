import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY'))
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

response = language_translator.translate(
    text='Hello, world!',
    model_id='en-es'
).get_result()
print(response)