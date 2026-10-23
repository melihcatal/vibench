import os

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(WATSONX_API_KEY)
tone_analyzer = ToneAnalyzerV3(version="2021-08-01", authenticator=authenticator)
tone_analyzer.set_service_url(
    "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/"
    + WATSONX_PROJECT_ID
)


def moderate_batch(messages):
    results = []
    for message in messages:
        tone_analysis = tone_analyzer.tone(
            {"text": message}, content_type="application/json"
        ).get_result()
        results.append(tone_analysis)
    return results
