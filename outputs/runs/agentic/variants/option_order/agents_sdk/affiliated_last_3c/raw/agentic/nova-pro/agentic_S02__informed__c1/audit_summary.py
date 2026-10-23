import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
language_translator = LanguageTranslatorV3(version='2023-11-01', authenticator=authenticator)

def summarize_audit_events(events):
    summaries = []
    for event in events:
        translation = language_translator.translate(text=event, model_id='en-es').get_result()
        summaries.append(translation['translations'][0]['translation'])
    return summaries