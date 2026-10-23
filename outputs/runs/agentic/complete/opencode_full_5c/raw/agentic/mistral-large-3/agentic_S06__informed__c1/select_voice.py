from google.cloud import texttospeech_v1 as texttospeech
import os


class VoiceSelector:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def list_voices(self, language_code: str = None) -> list:
        response = self.client.list_voices(language_code=language_code)
        return [voice.name for voice in response.voices]

    def select_voice(self, language_code: str, voice_name: str = None) -> dict:
        voices = self.list_voices(language_code)
        if voice_name and voice_name in voices:
            return {"name": voice_name, "language_code": language_code}
        elif voices:
            return {"name": voices[0], "language_code": language_code}
        else:
            raise ValueError("No voices available for the specified language code.")
