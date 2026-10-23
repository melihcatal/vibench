import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_URL = os.getenv('WATSONX_URL')

authenticator = IAMAuthenticator(WATSONX_API_KEY)
tone_analyzer = ToneAnalyzerV3(version='2021-07-29', authenticator=authenticator)
tone_analyzer.set_service_url(WATSONX_URL)

def moderation_summary(text):
    tone_analysis = tone_analyzer.tone({'text': text}, content_type='application/json').get_result()
    return tone_analysis
