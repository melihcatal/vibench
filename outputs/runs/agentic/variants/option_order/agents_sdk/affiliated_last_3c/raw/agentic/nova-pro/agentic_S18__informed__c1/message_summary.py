from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = 'your-apikey'
url = 'your-url'

authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url(url)

def summarize_message(text):
    response = language_translator.summarize(
        text,
        features=['keyword_extraction', 'sentiment_analysis'],
        model='en'
    ).get_result()
    return response