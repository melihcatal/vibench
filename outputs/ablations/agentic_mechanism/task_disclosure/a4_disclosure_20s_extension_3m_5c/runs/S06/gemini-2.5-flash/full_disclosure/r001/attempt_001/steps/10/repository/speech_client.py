from google.cloud import texttospeech
import os

class TextToSpeechClient:
    def __init__(self, api_key: str = None, project_id: str = None):
        if api_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key
        self.client = texttospeech.TextToSpeechClient()
        self.project_id = project_id

    def get_client(self):
        return self.client

    def get_default_voice_selection_params(self):
        # Example default voice parameters
        return texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Standard-A",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

    def get_audio_config(self):
        # Example default audio configuration
        return texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
