from google.cloud import texttospeech
from speech_client import TextToSpeechClient
from speech_models import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SynthesizeSpeechRequest,
    SynthesizeSpeechResponse,
)
import os


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_encoding: str = "MP3",
) -> SynthesizeSpeechResponse:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().client

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding)
    )

    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    response = client.synthesize_speech(request=request)
    return SynthesizeSpeechResponse(audio_content=response.audio_content)
