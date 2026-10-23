from google.cloud import texttospeech
from speech_client import get_speech_client
from speech_models import SynthesisRequest


def synthesize_text(request: SynthesisRequest) -> bytes:
    client = get_speech_client().tts_client

    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name if request.voice_name else "en-US-Standard-A",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_encoding)
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
