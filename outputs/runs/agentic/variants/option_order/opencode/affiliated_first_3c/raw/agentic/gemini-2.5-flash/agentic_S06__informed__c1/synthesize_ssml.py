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


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume_gain_db: float = 0.0,
) -> SynthesizeSpeechResponse:
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().client

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding),
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
    )

    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    response = client.synthesize_speech(request=request)
    return SynthesizeSpeechResponse(audio_content=response.audio_content)
