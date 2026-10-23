from dataclasses import dataclass
from google.cloud import texttospeech_v1 as tts
from typing import Union

@dataclass
class SynthesisRequest:
    input: tts.SynthesisInput
    voice: tts.VoiceSelectionParams
    audio_config: tts.AudioConfig

@dataclass
class SynthesisResponse:
    audio_content: bytes

def normalize_voice_name(voice_name: str) -> str:
    if not voice_name.startswith("en-US-"):
        return f"en-US-{voice_name}"
    return voice_name