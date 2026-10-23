from google.cloud import texttospeech_v1 as tts
import os


class TextToSpeechSynthesizer:
    def __init__(self):
        self.client = tts.TextToSpeechClient()
        self.voice_name = "en-US-Studio-O"

    def synthesize_text(self, text: str) -> bytes:
        input_text = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(language_code="en-US", name=self.voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content
