import os

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_tone(text):
    apikey = os.getenv("IBM_TONE_APIKEY")
    url = os.getenv("IBM_TONE_URL")

    authenticator = IAMAuthenticator(apikey)
    tone_analyzer = ToneAnalyzerV3(version="2017-09-21", authenticator=authenticator)
    tone_analyzer.set_service_url(url)

    tone = tone_analyzer.tone({"text": text}).get_result()
    return tone
