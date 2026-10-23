from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable

import requests
from google.cloud import texttospeech
from google.cloud import speech as gcloud_speech
from openai import OpenAI
from anthropic import Anthropic

from speech_models import (
    AudioSaveRequest,
    AudioSaveResponse,
    SsmlRequest,
    TextToSpeechRequest,
    TextToSpeechResponse,
    VoiceSelectionRequest,
    VoiceSelectionResponse,
)

DEFAULT_OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_AZURE_VOICE = "en-US-JennyNeural"
DEFAULT_GOOGLE_VOICE = "en-US-Standard-C"
DEFAULT_CONTENT_TYPE = "audio/mpeg"


def resolve_audio_format(audio_format: str) -> str:
    fmt = audio_format.strip().upper()
    if fmt in {"MP3", "MPEG"}:
        return "MP3"
    if fmt in {"OGG", "OGG_OPUS"}:
        return "OGG_OPUS"
    if fmt in {"LINEAR16", "WAV"}:
        return "LINEAR16"
    return "MP3"


def get_tts_client() -> "UnifiedSpeechClient":
    provider = os.getenv("TTS_PROVIDER", "google").strip().lower()
    return UnifiedSpeechClient(provider=provider)


@dataclass
class UnifiedSpeechClient:
    provider: str

    def synthesize_text(self, request: TextToSpeechRequest) -> TextToSpeechResponse:
        if self.provider == "openai":
            return self._synthesize_openai(request.text, request.voice_name, request.locale)
        if self.provider == "azure":
            return self._synthesize_azure(request.text, request.voice_name, request.locale, request.audio_format)
        return self._synthesize_google_text(request.text, request.voice_name, request.locale, request.audio_format)

    def synthesize_ssml(self, request: SsmlRequest) -> TextToSpeechResponse:
        if self.provider == "azure":
            return self._synthesize_azure(request.ssml, request.voice_name, request.locale, request.audio_format, is_ssml=True)
        return self._synthesize_google_ssml(request.ssml, request.voice_name, request.locale, request.audio_format)

    def select_voice(self, request: VoiceSelectionRequest) -> VoiceSelectionResponse:
        if self.provider == "google":
            return self._select_google_voice(request.locale, request.voice_name)
        if self.provider == "azure":
            return self._select_azure_voice(request.locale, request.voice_name)
        return self._select_openai_voice(request.locale, request.voice_name)

    def save_audio(self, request: AudioSaveRequest) -> AudioSaveResponse:
        if request.stream is not None:
            request.stream.write(request.audio_bytes)
            return AudioSaveResponse(path=None, bytes_written=len(request.audio_bytes), content_type=request.content_type)
        if request.output_path is None:
            raise ValueError("output_path or stream is required")
        path = Path(request.output_path)
        path.write_bytes(request.audio_bytes)
        return AudioSaveResponse(path=str(path), bytes_written=len(request.audio_bytes), content_type=request.content_type)

    def _synthesize_openai(self, text: str, voice_name: str | None, locale: str | None) -> TextToSpeechResponse:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        voice = voice_name or "alloy"
        result = client.audio.speech.create(model=DEFAULT_OPENAI_TTS_MODEL, voice=voice, input=text)
        audio_bytes = result.read()
        return TextToSpeechResponse(audio_bytes=audio_bytes, content_type=DEFAULT_CONTENT_TYPE, provider="openai", voice=voice, locale=locale)

    def _synthesize_google_text(self, text: str, voice_name: str | None, locale: str | None, audio_format: str) -> TextToSpeechResponse:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=locale or "en-US", name=voice_name or DEFAULT_GOOGLE_VOICE)
        audio_config = texttospeech.AudioConfig(audio_encoding=getattr(texttospeech.AudioEncoding, audio_format))
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        content_type = "audio/wav" if audio_format == "LINEAR16" else "audio/mpeg"
        return TextToSpeechResponse(audio_bytes=response.audio_content, content_type=content_type, provider="google", voice=voice.name, locale=voice.language_code)

    def _synthesize_google_ssml(self, ssml: str, voice_name: str | None, locale: str | None, audio_format: str) -> TextToSpeechResponse:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(language_code=locale or "en-US", name=voice_name or DEFAULT_GOOGLE_VOICE)
        audio_config = texttospeech.AudioConfig(audio_encoding=getattr(texttospeech.AudioEncoding, audio_format))
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        content_type = "audio/wav" if audio_format == "LINEAR16" else "audio/mpeg"
        return TextToSpeechResponse(audio_bytes=response.audio_content, content_type=content_type, provider="google", voice=voice.name, locale=voice.language_code)

    def _synthesize_azure(self, text: str, voice_name: str | None, locale: str | None, audio_format: str, is_ssml: bool = False) -> TextToSpeechResponse:
        endpoint = os.environ["AZURE_SPEECH_ENDPOINT"].rstrip("/")
        key = os.environ["AZURE_SPEECH_KEY"]
        voice = voice_name or DEFAULT_AZURE_VOICE
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/ssml+xml" if is_ssml else "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3" if audio_format == "MP3" else "riff-16khz-16bit-mono-pcm",
        }
        if is_ssml:
            body = text.encode("utf-8")
        else:
            body = f"<speak version='1.0' xml:lang='{locale or 'en-US'}'><voice name='{voice}'>{text}</voice></speak>".encode("utf-8")
        response = requests.post(f"{endpoint}/cognitiveservices/v1", headers=headers, data=body, timeout=60)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", DEFAULT_CONTENT_TYPE)
        return TextToSpeechResponse(audio_bytes=response.content, content_type=content_type, provider="azure", voice=voice, locale=locale)

    def _select_google_voice(self, locale: str | None, voice_name: str | None) -> VoiceSelectionResponse:
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices(language_code=locale or "en-US").voices
        selected = next((v for v in voices if voice_name and v.name == voice_name), voices[0] if voices else None)
        return VoiceSelectionResponse(provider="google", locale=locale, voice_name=selected.name if selected else None, voices=[v.name for v in voices])

    def _select_azure_voice(self, locale: str | None, voice_name: str | None) -> VoiceSelectionResponse:
        endpoint = os.environ["AZURE_SPEECH_ENDPOINT"].rstrip("/")
        key = os.environ["AZURE_SPEECH_KEY"]
        headers = {"Ocp-Apim-Subscription-Key": key}
        response = requests.get(f"{endpoint}/cognitiveservices/voices/list", headers=headers, timeout=60)
        response.raise_for_status()
        voices = response.json()
        filtered = [v["ShortName"] for v in voices if not locale or v.get("Locale") == locale]
        selected = voice_name if voice_name in filtered else (filtered[0] if filtered else None)
        return VoiceSelectionResponse(provider="azure", locale=locale, voice_name=selected, voices=filtered)

    def _select_openai_voice(self, locale: str | None, voice_name: str | None) -> VoiceSelectionResponse:
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        selected = voice_name if voice_name in voices else voices[0]
        return VoiceSelectionResponse(provider="openai", locale=locale, voice_name=selected, voices=voices)
