import os
from speech_client import get_text_to_speech_client
from speech_models import SSMLSynthesisInput

def synthesize_ssml(ssml: str, voice_name: str = None, audio_format: str = "mp3") -> bytes:
    """Synthesize SSML with voice and prosody controls via Azure AI Speech TTS.

    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.
    """
    client = get_text_to_speech_client()
    # Build input and voice config
    input_data = SSMLSynthesisInput(ssml=ssml)
    if voice_name:
        config = {
            "voice_name": voice_name,
            "audio_format": audio_format,
        }
    else:
        config = {"audio_format": audio_format}
    response = client.synthesize_speech(input=input_data, voice=config)
    return response.audio_content