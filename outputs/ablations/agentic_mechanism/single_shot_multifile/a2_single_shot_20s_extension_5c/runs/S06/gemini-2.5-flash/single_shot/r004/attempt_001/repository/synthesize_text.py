import os
from google.cloud import texttospeech
from speech_client import get_google_tts_client
from speech_models import SynthesisRequest, AudioResult

def synthesize_plain_text(request: SynthesisRequest) -> AudioResult:
    client = get_google_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding={
            "MP3": texttospeech.AudioEncoding.MP3,
            "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }.get(request.audio_encoding, texttospeech.AudioEncoding.MP3),
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioResult(
        audio_content=response.audio_content,
        audio_encoding=request.audio_encoding
    )
