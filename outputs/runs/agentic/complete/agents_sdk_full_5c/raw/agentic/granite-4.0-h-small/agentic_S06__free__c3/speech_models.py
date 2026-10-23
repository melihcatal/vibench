# speech_models.py
# [HELPER]
# Data models and validation utilities for Text-to-Speech request/response handling.

from typing import List, Tuple
from google.cloud.texttospeech import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SynthesizeSpeechResponse,
    Voice,
    AudioEncoding,
)

class TextToSpeechResponse:
    """Wrapper for SynthesizeSpeechResponse with basic validation."""
    def __init__(self, response: SynthesizeSpeechResponse):
        self.response = response

    def validate(self):
        """Simple sanity check."""
        if not self.response.audio_content:
            raise ValueError("Synthesized audio content is empty")

# Re‑export basic protobuf model classes for convenience
SynthesisInput = SynthesisInput
VoiceSelectionParams = VoiceSelectionParams
AudioConfig = AudioConfig
Voice = Voice
AudioEncoding = AudioEncoding
