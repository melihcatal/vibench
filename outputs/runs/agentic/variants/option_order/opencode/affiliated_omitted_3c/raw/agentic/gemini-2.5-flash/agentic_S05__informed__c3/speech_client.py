import os
import azure.cognitiveservices.speech as speechsdk


class SpeechClient:
    def __init__(self):
        self.speech_key = os.environ.get("AZURE_SPEECH_KEY")
        self.service_region = os.environ.get("AZURE_SPEECH_REGION")
        if not self.speech_key or not self.service_region:
            raise ValueError(
                "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
            )
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.service_region
        )

    def get_speech_recognizer(
        self, audio_config: speechsdk.AudioConfig, language: str = "en-US"
    ):
        self.speech_config.speech_recognition_language = language
        return speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
