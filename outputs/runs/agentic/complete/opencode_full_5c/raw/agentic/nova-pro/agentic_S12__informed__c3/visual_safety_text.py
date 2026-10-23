from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def visual_safety_text(text):
    authenticator = IAMAuthenticator("WATSONX_API_KEY")
    tone_analyzer = ToneAnalyzerV3(version="2021-09-01", authenticator=authenticator)
    tone_analysis = tone_analyzer.tone(
        {"text": text}, content_type="application/json"
    ).get_result()
    return tone_analysis
