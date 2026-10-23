import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def unsafe_copy_check(text):
    api_key = os.getenv("WATSONX_API_KEY")
    url = os.getenv("WATSONX_URL")
    authenticator = IAMAuthenticator(api_key)
    tone_analyzer = ToneAnalyzerV3(version="2017-09-21", authenticator=authenticator)
    tone_analyzer.set_service_url(url)
    tone = tone_analyzer.tone(text=text, content_type="text/plain").get_result()
    return tone
