from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = "your-watsonx-api-key"
WATSONX_PROJECT_ID = "your-watsonx-project-id"

authenticator = IAMAuthenticator(WATSONX_API_KEY)
tone_analyzer = ToneAnalyzerV3(version="2023-04-04", authenticator=authenticator)
tone_analyzer.set_service_url(
    "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/your-instance-id"
)


def visual_safety_text(text):
    tone_analysis = tone_analyzer.tone({"text": text}).get_result()
    return tone_analysis
