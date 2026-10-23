import os
from typing import Optional
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_speech_client() -> Optional[TextToSpeechV1]:
    api_key = os.getenv("IBM_TTS_APIKEY")
    url = os.getenv("IBM_TTS_URL")
    
    if not api_key or not url:
        return None
    
    authenticator = IAMAuthenticator(api_key)
    client = TextToSpeechV1(authenticator=authenticator)
    client.set_service_url(url)
    return client