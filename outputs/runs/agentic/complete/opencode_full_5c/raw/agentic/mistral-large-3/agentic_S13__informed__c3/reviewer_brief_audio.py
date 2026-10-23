from typing import Dict
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import os


def reviewer_brief_audio(brief_text: str, output_file: str) -> None:
    """Generate spoken briefs for moderation reviewers using Azure Speech TTS."""
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    audio_config = AudioConfig(filename=output_file)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    synthesizer.speak_text(brief_text)
