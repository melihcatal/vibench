# [LATER-STEP] retrieval_audio_brief.py
# Generate a spoken brief from retrieved search results

# Identifiable provider: Azure Speech (Text-to-Speech)
import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
if not (SPEECH_KEY and SPEECH_REGION):
    raise RuntimeError("Azure Speech keys not configured")

def generate_audio_brief(text: str) -> bytes:
    """
    Convert plain text into an audio (WAV) byte payload using Azure Speech TTS.
    Returns raw audio bytes suitable for saving or streaming.
    """
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = AudioConfig(output_format="RiffPcm", output_format="Riff16Khz16BitMonoPcm")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text(text)
    if result.reason == result.reason_success:
        return result.audio_data
    else:
        raise RuntimeError(f"TTS failed with reason: {result.reason}")
