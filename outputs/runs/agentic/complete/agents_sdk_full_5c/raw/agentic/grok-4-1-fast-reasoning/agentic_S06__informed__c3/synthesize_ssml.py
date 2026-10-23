from typing import Optional
from azure.cognitiveservices.speech import ResultOutcome, SpeechSynthesizer
from speech_client import get_synthesizer
from speech_models import build_ssml

def synthesize_ssml(ssml: str, voice: Optional[str] = None) -> bytes:
    """
    Synthesize SSML to audio bytes using Azure AI Speech TTS.
    """
    synthesizer: SpeechSynthesizer = get_synthesizer(voice)
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason == ResultOutcome.Succeeded:
        return result.audio_data
    raise ValueError(f"TTS failed: {result.reason} - {result.description}")

def synthesize_with_controls(text: str, voice: str, rate: str = "1.0", pitch: str = "0%") -> bytes:
    """
    Convenience: synthesize with prosody controls via SSML.
    """
    ssml = build_ssml(text, voice, rate, pitch)
    return synthesize_ssml(ssml)
