# Generate Spoken Briefs for Moderation Reviewers
from google.cloud import texttospeech_v1 as tts
from typing import Optional


class ReviewerBriefAudioGenerator:
    def __init__(self):
        self.client = tts.TextToSpeechClient()

    def generate_audio_brief(
        self, text: str, output_file: str, voice_name: Optional[str] = "en-US-Wavenet-D"
    ) -> None:
        """Generate spoken brief using Google Cloud Text-to-Speech API."""
        synthesis_input = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(
            language_code="en-US", name=voice_name
        )
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(output_file, "wb") as out:
            out.write(response.audio_content)