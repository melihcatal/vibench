import os
import azure.cognitiveservices.speech as speechsdk

class SpeechClient:
    def __init__(self):
        self.subscription_key = os.getenv('AZURE_SPEECH_KEY')
        self.region = os.getenv('AZURE_SPEECH_REGION')
        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.region)

    def get_speech_recognizer(self, audio_config):
        return speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
