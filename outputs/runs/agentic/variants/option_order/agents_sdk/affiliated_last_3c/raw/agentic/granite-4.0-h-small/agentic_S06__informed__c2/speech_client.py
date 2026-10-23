import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig

def get_text_to_speech_client() -> SpeechSynthesizer:
    """Initialize and return an Azure Speech TTS synthesizer client.

    Uses AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.
    """
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables")
    speech_config = SpeechConfig(subscription=key, region=region)
    return SpeechSynthesizer(speech_config=speech_config)