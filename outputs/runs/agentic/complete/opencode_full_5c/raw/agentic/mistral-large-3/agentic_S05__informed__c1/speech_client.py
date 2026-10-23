import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Optional


def get_speech_client() -> SpeechToTextV1:
    """
    Provides a configured IBM Watson STT client.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    client = SpeechToTextV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_STT_URL"))
    return client


class StreamingRecognitionConfig:
    """
    Configuration for IBM Watson STT streaming recognition.
    """

    def __init__(
        self,
        model: str = "en-US_Multimedia",
        interim_results: bool = True,
        smart_formatting: bool = True,
        content_type: str = "audio/l16; rate=44100",
    ):
        self.model = model
        self.interim_results = interim_results
        self.smart_formatting = smart_formatting
        self.content_type = content_type
