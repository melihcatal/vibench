from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("your-watson-api-key")
tone_analyzer = ToneAnalyzerV3(version="2021-08-01", authenticator=authenticator)


def onboarding_summary(text):
    tone_analysis = tone_analyzer.tone({"text": text}).get_result()
    return tone_analysis["document_tone"]["tones"]
