import os
from elevenlabs.client import ElevenLabs
from speech_client import get_elevenlabs_client
from speech_models import SynthesisRequest


def synthesize_text_to_audio(request: SynthesisRequest) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using ElevenLabs.
    """
    client: ElevenLabs = get_elevenlabs_client()

    audio = client.generate(
        text=request.text, voice=request.voice_id, model=request.model_id
    )
    return audio
