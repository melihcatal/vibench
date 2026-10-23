# retrieval_audio_brief.py - LATER-STEP
# Generate a spoken brief from retrieved search results using Azure Speech TTS

import os
import json
from typing import List

# Example provider: Azure AI Speech (Text-to-Speech) SDK
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
if not (AZURE_SPEECH_KEY and AZURE_SPEECH_REGION):
    raise ValueError("Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION")

from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioConfiguration,
    SpeechSynthesizer,
)

_config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)

_synthesizer = SpeechSynthesizer(speech_config=_config)


def generate_audio_brief(text: str) -> bytes:
    """
    Synthesize the provided text into an audio byte stream (WAV).

    Returns:
        bytes: Audio data ready for playback or saving to a file.
    """
    result = _synthesizer.speak_text_async(text).get()
    # Convert to bytes (Azure SDK returns bytes already)
    return result.audio_data
