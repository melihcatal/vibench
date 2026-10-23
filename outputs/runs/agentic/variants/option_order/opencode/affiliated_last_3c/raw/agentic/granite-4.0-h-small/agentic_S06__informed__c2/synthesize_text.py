# [SAME-SCENARIO] synthesize_text.py
# Azure Speech TTS integration
import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Load credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def synthesize_text(plain_text: str, voice_name: str = "en-US-JennyNeural") -> bytes:
    """Synthesize plain text to an audio byte stream using Azure Cognitive Services Speech SDK.

    Args:
        plain_text (str): The text to synthesize.
        voice_name (str): The voice name to use (default: en-US-JennyNeural).

    Returns:
        bytes: The synthesized audio as an MP3 byte stream.
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    speech_config.speech_synthesis_voice_name = voice_name
    audio_config = AudioConfig(output_format="Mp3")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(plain_text).get()
    if result.reason == result.reasons_success:
        return result.audio_data
    else:
        raise RuntimeError(f"Synthesis failed: {result.reason}")
