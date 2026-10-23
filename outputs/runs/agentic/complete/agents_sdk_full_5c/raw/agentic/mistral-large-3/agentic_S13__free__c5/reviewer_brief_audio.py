import os
from typing import Optional
from google.cloud import texttospeech_v1 as tts


class ReviewerBriefAudioGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required.")
        self.client = tts.TextToSpeechClient()

    def generate_audio(self, text: str, output_file: str) -> None:
        synthesis_input = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D"
        )
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(output_file, "wb") as out:
            out.write(response.audio_content)


def generate_reviewer_brief_audio(text: str, output_file: str) -> None:
    generator = ReviewerBriefAudioGenerator()
    generator.generate_audio(text, output_file)