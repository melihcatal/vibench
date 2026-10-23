from google.cloud import texttospeech_v1 as tts
import os


class VoiceSelector:
    def __init__(self):
        self.client = tts.TextToSpeechClient()

    def list_voices(self, language_code: str = None) -> list:
        response = self.client.list_voices(language_code=language_code)
        return [voice.name for voice in response.voices]

    def select_voice(self, language_code: str, voice_name: str = None) -> dict:
        voices = self.client.list_voices(language_code=language_code)
        for voice in voices.voices:
            if voice_name and voice.name == voice_name:
                return {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": tts.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
        return {
            "name": voices.voices[0].name,
            "language_codes": voices.voices[0].language_codes,
            "ssml_gender": tts.SsmlVoiceGender(voices.voices[0].ssml_gender).name,
            "natural_sample_rate_hertz": voices.voices[0].natural_sample_rate_hertz,
        }
