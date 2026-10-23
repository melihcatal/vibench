import os
from typing import Any, Dict, List, Optional

from google.cloud import texttospeech

from speech_models import SynthesisRequest, SynthesisResponse, normalize_text


def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def build_voice_params(language_code: str, voice_name: Optional[str] = None) -> texttospeech.VoiceSelectionParams:
    kwargs: Dict[str, Any] = {"language_code": language_code}
    if voice_name:
        kwargs["name"] = voice_name
    return texttospeech.VoiceSelectionParams(**kwargs)


def build_audio_config() -> texttospeech.AudioConfig:
    return texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)


def synthesize(request: SynthesisRequest) -> SynthesisResponse:
    client = get_client()
    input_text = texttospeech.SynthesisInput(ssml=request.text) if request.ssml else texttospeech.SynthesisInput(text=normalize_text(request.text))
    voice = build_voice_params(request.language_code, request.voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return SynthesisResponse(audio_content=response.audio_content, mime_type="audio/mpeg", voice_name=request.voice_name)


def list_voices(language_code: Optional[str] = None) -> List[str]:
    client = get_client()
    response = client.list_voices(language_code=language_code) if language_code else client.list_voices()
    return [voice.name for voice in response.voices]


def default_language_code() -> str:
    return os.getenv("GOOGLE_TTS_LANGUAGE_CODE", "en-US")
