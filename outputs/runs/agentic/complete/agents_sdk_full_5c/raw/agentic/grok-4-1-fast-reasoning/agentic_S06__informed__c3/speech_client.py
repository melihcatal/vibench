import os
from typing import Optional
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

def get_speech_config() -> SpeechConfig:
    """Get Azure Speech Config."""
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    if not key or not region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set.")
    return SpeechConfig(subscription=key, region=region)

def get_synthesizer(voice_name: Optional[str] = None) -> SpeechSynthesizer:
    """Get Azure Speech Synthesizer optionally with voice."""
    config = get_speech_config()
    if voice_name:
        config.speech_synthesis_voice_name = voice_name
    return SpeechSynthesizer(speech_config=config)
