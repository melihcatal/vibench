import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from google.cloud import texttospeech

from speech_models import SpeechRequest, SpeechResponse, normalize_ssml, normalize_text


def get_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def build_audio_config(
    speaking_rate: Optional[float] = None, pitch: Optional[float] = None
):
    kwargs = {}
    if speaking_rate is not None:
        kwargs["speaking_rate"] = speaking_rate
    if pitch is not None:
        kwargs["pitch"] = pitch
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, **kwargs
    )


def build_voice_params(
    language_code: Optional[str] = None, voice_name: Optional[str] = None
):
    kwargs: Dict[str, Any] = {}
    if language_code:
        kwargs["language_code"] = language_code
    if voice_name:
        kwargs["name"] = voice_name
    return texttospeech.VoiceSelectionParams(**kwargs)


def synthesize_request(request: SpeechRequest) -> SpeechResponse:
    client = get_tts_client()
    voice = build_voice_params(request.language_code, request.voice_name)
    audio_config = build_audio_config(request.speaking_rate, request.pitch)
    input_text = (
        normalize_ssml(request.text) if request.ssml else normalize_text(request.text)
    )
    synthesis_input = (
        texttospeech.SynthesisInput(ssml=input_text)
        if request.ssml
        else texttospeech.SynthesisInput(text=input_text)
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return SpeechResponse(
        audio_bytes=response.audio_content,
        content_type="audio/mpeg",
        metadata={"request": asdict(request)},
    )
