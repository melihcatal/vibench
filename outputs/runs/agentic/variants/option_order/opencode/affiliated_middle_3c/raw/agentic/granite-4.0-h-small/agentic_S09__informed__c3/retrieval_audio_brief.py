import os
from text_to_speech_client import (
    TextToSpeechClient,
)  # placeholder client for concrete provider


def generate_audio_brief(retrieved: list[str]) -> str:
    """Create a spoken brief from retrieved search results.

    Concatenates result snippets and passes the text to a TTS provider (Azure Speech TTS as example).
    Returns the path to the generated audio file (or audio binary if provider returns bytes).
    """
    client = TextToSpeechClient()
    client.set_provider("azure-speech-tts")
    # Simple concatenation of results
    brief_text = "Result brief: " + " | ".join(retrieved)
    audio_file = client.synthesize(brief_text)
    return audio_file
