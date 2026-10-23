import os
import wave
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Azure TTS configuration (keys/region loaded from env)
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

def synthesize_text(text: str, voice_name: str = None) -> bytes:
    """Synthesize plain text to raw PCM audio bytes using Azure Speech TTS.

    Args:
        text: Plain text to speak.
        voice_name: Optional voice name (e.g., "en-US-JaneNeural").

    Returns:
        Audio bytes (PCM 16-bit mono).
    """
    speech_config = SpeechConfig(endpoint="https://eastus.tts.speech.microsoft.com", subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    audio_config = AudioConfig(output_format=AudioConfig.audio_output_format="Riff16Khz16BitMonoPcm")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data  # bytes
