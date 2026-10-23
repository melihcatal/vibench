import os
from google.cloud import texttospeech  # Google Cloud Text-to-Speech SDK

class TextToSpeechClient:
    def __init__(self):
        # credentials are read from GOOGLE_APPLICATION_CREDENTIALS env var
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, input_text, voice_name=None, audio_format='LINEAR16'):
        """
        Synthesizes plain text or SSML to an AudioContent object.
        Args:
            input_text (str): Plain text or SSML payload.
            voice_name (str | None): Optional specific voice ID.
            audio_format (str): Audio encoding, e.g., LINEAR16, MP3.
        Returns:
            google.cloud.texttospeech_v1.types.SynthesizeSpeechResponse
        """
        synthesis_input = texttospeech.SynthesisInput(text=input_text)
        # If no voice_name, use default; otherwise pick a specific voice later via select_voice.py
        voice_config = texttospeech.VoiceSelectionParams() if voice_name is None else texttospeech.VoiceSelectionParams(name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=getattr(texttospeech.AudioEncoding, audio_format))
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice_config,
            output_config=audio_config
        )
        return response
