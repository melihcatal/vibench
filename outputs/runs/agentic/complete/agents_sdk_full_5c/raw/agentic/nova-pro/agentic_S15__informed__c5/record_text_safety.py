import os
import ibm_watson
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions

authenticator = ibm_watson.IAMAuthenticator(os.environ['WATSONX_API_KEY'])
nlu = ibm_watson.NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url(os.environ['WATSONX_URL'])

def check_text_safety(text):
    response = nlu.analyze(
        text=text,
        features=Features(emotion=EmotionOptions(), sentiment=SentimentOptions())
    ).get_result()
    return response