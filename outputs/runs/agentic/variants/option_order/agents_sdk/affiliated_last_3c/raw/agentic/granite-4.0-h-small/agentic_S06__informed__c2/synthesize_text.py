import os
from speech_client import get_text_to_speech_client
from speech_models import SynthesisInput

def synthesize_text(text: str, voice_name: str = None, audio_format: str = "mp3") -> bytes:
    """Synthesizes plain text to an audio byte stream using a concrete provider.

    Here we use Azure AI Speech TTS as the provider.
    Requires environment variables AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.
    """
    client = get_text_to_speech_client()
    # Configure synthesis input
    input_data = SynthesisInput(text=text)
    # Choose voice; if none provided, default to the service default
    if voice_name:
        config = {
            "voice_name": voice_name,
            "audio_format": audio_format,
        }
    else:
        config = {"audio_format": audio_format}
    response = client.synthesize_speech(input=input_data, voice=config)
    # The SDK returns binary audio data
    return response.audio_content