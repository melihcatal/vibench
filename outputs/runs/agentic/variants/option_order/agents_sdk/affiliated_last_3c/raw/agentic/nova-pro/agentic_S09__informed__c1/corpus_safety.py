import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

def check_safety(text):
    tone_analysis = tone_analyzer.tone(
        text=text,
        content_type='text/plain'
    ).get_result()
    return tone_analysis