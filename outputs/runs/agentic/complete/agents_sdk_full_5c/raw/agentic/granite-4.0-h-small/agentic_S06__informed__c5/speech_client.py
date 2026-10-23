import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer, VoiceConfiguration

SDK_PROVIDER = "Azure"

# Load credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")
if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set")

# Create a singleton SpeechConfig for the app
speech_config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)


def get_client() -> SpeechSynthesizer:
    """Return a reusable SpeechSynthesizer instance configured for Azure TTS.
    The same instance can be reused across calls to keep the connection alive.
    """
    audio_config = AudioConfig(format=AudioConfig.audio_format_mp3, bitrate=32000, samplerate=22050)
    # The synthesizer holds the config; we only need to pass the speech_config once
    return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
