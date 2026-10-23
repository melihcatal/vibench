from google.cloud import texttospeech

from speech_client import (
    default_audio_encoding,
    default_language_code,
    default_voice_name,
    get_client,
)
from speech_models import TTSRequest, TTSResponse, normalize_text


def synthesize_text(
    text: str, voice: str = None, language_code: str = None, audio_encoding: str = None
) -> bytes:
    request = TTSRequest(
        text=normalize_text(text),
        voice=voice or default_voice_name(),
        locale=language_code or default_language_code(),
    )
    client = get_client()
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=request.locale or "en-US",
        name=request.voice or "en-US-Neural2-A",
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


def synthesize_text_response(
    text: str, voice: str = None, language_code: str = None, audio_encoding: str = None
) -> TTSResponse:
    audio = synthesize_text(
        text, voice=voice, language_code=language_code, audio_encoding=audio_encoding
    )
    return TTSResponse(
        audio=audio, voice=voice or default_voice_name(), content_type="audio/mpeg"
    )
