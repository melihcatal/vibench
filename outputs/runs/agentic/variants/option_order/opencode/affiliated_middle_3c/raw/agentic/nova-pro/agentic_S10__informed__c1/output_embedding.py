import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = os.environ["IBM_API_KEY_ID"]
url = os.environ["IBM_URL"]

authenticator = IAMAuthenticator(apikey)
tone_analyzer = ToneAnalyzerV3(version="2017-09-21", authenticator=authenticator)

tone_analyzer.set_service_url(url)


def analyze_tone(text):
    tone_analysis = tone_analyzer.tone({"text": text}).get_result()
    return tone_analysis
