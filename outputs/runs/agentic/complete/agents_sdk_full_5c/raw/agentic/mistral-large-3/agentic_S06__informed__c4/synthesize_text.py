from typing import Iterator
import os
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_text(text: str, voice_id: str = "alloy", model: str = "tts-1") -> Iterator[bytes]:
    """
    Synthesize plain text to an audio byte stream using ElevenLabs.
    """
    client = get_speech_client()
    request = SynthesisRequest(text=text, voice_id=voice_id, model=model)
    
    response = client.text_to_speech.convert(
        voice_id=request.voice_id,
        output_format="pcm_16000",
        text=request.text,
        model_id=request.model
    )
    
    for chunk in response:
        if chunk:
            yield chunk


def synthesize_text_to_bytes(text: str, voice_id: str = "alloy", model: str = "tts-1") -> bytes:
    """
    Synthesize plain text to a single audio bytes object using ElevenLabs.
    """
    return b"".join(synthesize_text(text, voice_id, model))