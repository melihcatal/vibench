import os
import azure.cognitiveservices.speech as speechsdk


class SpeechClient:
    def __init__(self):
        self.speech_key = os.environ.get("AZURE_SPEECH_KEY")
        self.service_region = os.environ.get("AZURE_SPEECH_REGION")
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.service_region
        )

    def get_speech_config(self):
        return self.speech_config
