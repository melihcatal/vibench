import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, Iterable, List, Optional

from openai import AsyncOpenAI

from speech_models import SpeechRequest, TranscriptChunk, normalize_language, normalize_text


@dataclass
class SpeechClientConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"
    language: Optional[str] = None
    enable_punctuation: bool = True


def load_config(**overrides: Any) -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=overrides.get("api_key") or os.getenv("OPENAI_API_KEY"),
        model=overrides.get("model") or os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        language=normalize_language(overrides.get("language") or os.getenv("SPEECH_LANGUAGE")),
        enable_punctuation=bool(overrides.get("enable_punctuation", True)),
    )


def create_client(config: Optional[SpeechClientConfig] = None) -> AsyncOpenAI:
    config = config or load_config()
    return AsyncOpenAI(api_key=config.api_key)


async def stream_transcript_events(audio_chunks: AsyncIterator[bytes], request: Optional[SpeechRequest] = None) -> AsyncIterator[TranscriptChunk]:
    request = request or SpeechRequest()
    config = load_config(language=request.language, enable_punctuation=request.enable_punctuation, model=request.model)
    client = create_client(config)
    parts: List[bytes] = []
    async for chunk in audio_chunks:
        parts.append(chunk)
    audio_bytes = b"".join(parts)
    response = await client.audio.transcriptions.create(
        model=config.model,
        file=("audio.wav", audio_bytes),
        language=config.language,
        response_format="verbose_json",
        extra_body={"include_punctuation": config.enable_punctuation},
    )
    text = normalize_text(getattr(response, "text", ""))
    if text:
        yield TranscriptChunk(text=text, is_final=True, language=config.language, metadata={"provider": "openai"})
