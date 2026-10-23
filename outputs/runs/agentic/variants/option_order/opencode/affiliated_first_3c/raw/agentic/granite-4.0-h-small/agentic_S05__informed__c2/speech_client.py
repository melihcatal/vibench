import os
from ibm_cloud_sdk_core import IAMTokenManager
from ibm_watson import SpeechToTextV1

# Configuration (environment variables)
API_KEY = os.getenv("IBM_STT_APIKEY")
URL = os.getenv("IBM_STT_URL")


# Helper to obtain a fresh IAM token
def get_iam_token() -> str:
    iam_auth = IAMTokenManager(apikey=API_KEY)
    token = iam_auth.get_token()
    return token


# Watson STT client wrapper
class SpeechClient:
    def __init__(self):
        self.url = URL
        self.auth = get_iam_token()
        self.service = SpeechToTextV1(authenticator=IAMTokenManager(API_KEY))
        self.service.set_service_url(self.url)

    def recognize_stream(
        self,
        audio_provider,
        *,
        content_type="audio/l16; rate=16000",
        model="en-US_BroadbandModel",
        interim_results=True,
        continuous=True,
    ):
        """Start streaming recognition using the IBM SDK."""
        return self.service.recognize_stream(
            audio=audio_provider,
            content_type=content_type,
            model=model,
            interim_results=interim_results,
            continuous=continuous,
            auth_type="iam",
            headers={"Authorization": f"Bearer {self.auth}"},
        )


# Example usage (run with asyncio):
# client = SpeechClient()
# events = client.recognize_stream(audio_provider=MicrophoneStream())
# for event in events:
#     print(event)
