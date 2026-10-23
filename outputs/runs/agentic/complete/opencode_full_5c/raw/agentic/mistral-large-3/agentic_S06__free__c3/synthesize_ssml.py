from google.cloud import texttospeech_v1 as tts
import os


class SSMLToSpeechSynthesizer:
    def __init__(self):
        self.client = tts.TextToSpeechClient()
        self.voice_name = "en-US-Studio-O"

    def synthesize_ssml(self, ssml: str) -> bytes:
        input_text = tts.SynthesisInput(ssml=ssml)
        voice = tts.VoiceSelectionParams(language_code="en-US", name=self.voice_name)
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3,
            effects_profile_id=["small-bluetooth-speaker-class-device"],
        )
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content
