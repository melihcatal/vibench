from google.cloud import texttospeech_v1 as texttospeech
import os


class SSMLSynthesizer:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_ssml(
        self, ssml: str, language_code: str = "en-US", voice_name: str = None
    ) -> bytes:
        input_text = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content
