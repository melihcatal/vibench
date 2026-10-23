import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

os.environ['IBM_API_KEY_ID'] = 'your-ibm-api-key'

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-05-01',
    authenticator=authenticator
)

url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/your-instance-id'
natural_language_understanding.set_service_url(url)

def embed_translation_memory(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions())
    ).get_result()
    return response