from typing import Iterator
import os
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_ssml(ssml: str, voice_id: str = "alloy", model: str = "tts-1") -> Iterator[bytes]:
    """
    Synthesize SSML with voice and prosody controls using ElevenLabs.
    """
    client = get_speech_client()
    request = SynthesisRequest(text=ssml, voice_id=voice_id, model=model, is_ssml=True)
    
    response = client.text_to_speech.convert(
        voice_id=request.voice_id,
        output_format="pcm_16000",
        text=request.text,
        model_id=request.model,
        enable_ssml=True
    )
    
    for chunk in response:
        if chunk:
            yield chunk


def synthesize_ssml_to_bytes(ssml: str, voice_id: str = "alloy", model: str = "tts-1") -> bytes:
    """
    Synthesize SSML to a single audio bytes object using ElevenLabs.
    """
    return b"".join(synthesize_ssml(ssml, voice_id, model))