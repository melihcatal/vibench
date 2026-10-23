import os
from typing import Optional
from azure.cognitiveservices.speech import ResultOutcome, SpeechSynthesizer
from speech_client import get_synthesizer

def synthesize_text(text: str, voice: Optional[str] = None) -> bytes:
    """
    Synthesize plain text to audio bytes using Azure AI Speech TTS.
    """
    synthesizer: SpeechSynthesizer = get_synthesizer(voice)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == ResultOutcome.Succeeded:
        return result.audio_data
    raise ValueError(f"TTS failed: {result.reason} - {result.description}")
