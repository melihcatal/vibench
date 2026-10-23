import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

def summarize_job(job_id):
    translation = language_translator.translate(
        text='Job summary for job ID: ' + job_id,
        model_id='en-es'
    ).get_result()
    return translation['translations'][0]['translation']