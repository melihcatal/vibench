import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
language_translator = LanguageTranslatorV3(version='2023-04-01', authenticator=authenticator)

def summarize_incident(log_entries):
    translation = language_translator.translate(
        text=log_entries,
        model_id='en-es'
    ).get_result()
    return translation

log_entries = 'This is an example log entry for incident summary.'
summary = summarize_incident(log_entries)
print(summary)