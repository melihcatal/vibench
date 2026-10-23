from google.cloud import texttospeech

from speech_client import (
    default_audio_encoding,
    default_language_code,
    default_voice_name,
    get_client,
)
from speech_models import TTSResponse, normalize_ssml


def synthesize_ssml(
    ssml: str, voice: str = None, language_code: str = None, audio_encoding: str = None
) -> bytes:
    client = get_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=normalize_ssml(ssml))
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code or default_language_code() or "en-US",
        name=voice or default_voice_name() or "en-US-Neural2-A",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(
            texttospeech.AudioEncoding,
            (audio_encoding or default_audio_encoding()).upper(),
            texttospeech.AudioEncoding.MP3,
        )
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )
    return response.audio_content


def synthesize_ssml_response(
    ssml: str, voice: str = None, language_code: str = None, audio_encoding: str = None
) -> TTSResponse:
    audio = synthesize_ssml(
        ssml, voice=voice, language_code=language_code, audio_encoding=audio_encoding
    )
    return TTSResponse(
        audio=audio, voice=voice or default_voice_name(), content_type="audio/mpeg"
    )
