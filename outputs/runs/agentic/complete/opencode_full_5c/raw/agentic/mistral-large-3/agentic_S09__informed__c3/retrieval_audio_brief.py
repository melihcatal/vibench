import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from typing import List, Dict, Any


def generate_spoken_brief(text: str, output_file: str) -> None:
    """Generate a spoken brief from retrieved search results using Azure Speech TTS."""
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    audio_config = AudioConfig(filename=output_file)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesizer.speak_text(text)
