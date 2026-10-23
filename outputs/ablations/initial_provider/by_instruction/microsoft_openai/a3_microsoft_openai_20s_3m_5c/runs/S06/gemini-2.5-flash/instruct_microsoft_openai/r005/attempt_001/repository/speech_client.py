import os
from openai import OpenAI
import azure.cognitiveservices.speech as speechsdk

class SpeechClient:
    def __init__(self):
        self.openai_client = None
        self.azure_speech_config = None

    def get_openai_client(self) -> OpenAI:
        if not self.openai_client:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            self.openai_client = OpenAI(api_key=api_key)
        return self.openai_client

    def get_azure_speech_config(self) -> speechsdk.SpeechConfig:
        if not self.azure_speech_config:
            speech_key = os.environ.get("SPEECH_KEY")
            speech_region = os.environ.get("SPEECH_REGION")
            if not speech_key or not speech_region:
                raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set for Azure Speech.")
            self.azure_speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        return self.azure_speech_config
