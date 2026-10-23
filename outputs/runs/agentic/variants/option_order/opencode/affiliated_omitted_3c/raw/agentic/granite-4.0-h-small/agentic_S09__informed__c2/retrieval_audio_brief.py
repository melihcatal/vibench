import os
import requests
from pydub import AudioSegment

# Identifier: Azure Speech TTS SDK

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
if not all([AZURE_SPEECH_KEY, AZURE_SPEECH_REGION]):
    raise RuntimeError("Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION")

from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer


def retrieval_audio_brief(search_results: list) -> None:
    """Generate a spoken audio brief summarising the top search results.

    Args:
        search_results: List of dicts, each with 'title' and 'snippet' keys.
    "+   Writes an MP3 file 'retrieval_brief.mp3' to the current working directory.
    """
    # Simple concatenation of titles and snippets
    text = ""
    for i, result in enumerate(search_results, start=1):
        text += f"Result {i}: {result.get('title', 'untitled')}. "
        text += f"{result.get('snippet', '')} "
    # Initialize TTS client
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    audio_config = AudioConfig(filename="retrieval_brief.mp3")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    synthesizer.speak_text_async(text).get()
    print("Audio brief written to retrieval_brief.mp3")
