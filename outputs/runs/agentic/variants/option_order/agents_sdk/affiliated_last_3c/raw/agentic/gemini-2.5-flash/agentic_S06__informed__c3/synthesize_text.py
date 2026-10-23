
import os
from google.cloud import texttospeech
from speech_client import TextToSpeechClient
from speech_models import SynthesisRequest

def synthesize_text(request: SynthesisRequest) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        request: A SynthesisRequest object containing text and voice parameters.

    Returns:
        Audio content as bytes.
    """
    client_wrapper = TextToSpeechClient()
    client = client_wrapper.client

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, # Google Cloud Text-to-Speech specific enum
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
        sample_rate_hertz=request.sample_rate_hertz
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content
