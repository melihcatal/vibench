from typing import Optional, Union, BinaryIO
import os
from google.cloud import texttospeech_v1 as texttospeech
from google.api_core.exceptions import GoogleAPICallError


class TextToSpeechSynthesizer:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_text(
        self,
        text: str,
        voice_name: str = "en-US-Wavenet-D",
        language_code: str = "en-US",
        audio_encoding: str = "MP3",
    ) -> bytes:
        """
        Synthesizes plain text to an audio byte stream.

        Args:
            text: The plain text to synthesize.
            voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").
            language_code: The language code of the voice (e.g., "en-US").
            audio_encoding: The audio encoding format (e.g., "MP3", "LINEAR16").

        Returns:
            bytes: The synthesized audio content.

        Raises:
            GoogleAPICallError: If the synthesis fails.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding)
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
