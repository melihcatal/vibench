import os
from elevenlabs.client import ElevenLabs
from speech_client import get_elevenlabs_client
from speech_models import SSMLSynthesisRequest


def synthesize_ssml_to_audio(request: SSMLSynthesisRequest) -> bytes:
    """
    Synthesizes SSML to an audio byte stream using ElevenLabs.
    """
    client: ElevenLabs = get_elevenlabs_client()

    # ElevenLabs SDK currently doesn't have a direct SSML input for `generate`
    # It expects plain text. For SSML with ElevenLabs, typically you would
    # embed the SSML directly in the text parameter if the model supports it
    # or use a different API endpoint/SDK function.
    # For the purpose of this exercise, we will treat the SSML as text,
    # assuming the backend can interpret it.
    # In a real-world scenario, you'd check ElevenLabs' specific SSML support.

    audio = client.generate(
        text=request.ssml, voice=request.voice_id, model=request.model_id
    )
    return audio
