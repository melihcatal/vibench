from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from openai import OpenAI


OPENAI_WHISPER_MODEL = "whisper-1"


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None


def _resolve_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    kwargs = {}
    key = api_key or os.getenv("OPENAI_API_KEY")
    url = base_url or os.getenv("OPENAI_BASE_URL")
    if key:
        kwargs["api_key"] = key
    if url:
        kwargs["base_url"] = url
    return OpenAI(**kwargs)


def transcribe_qa_sample(audio, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = OPENAI_WHISPER_MODEL) -> str:
    client = _resolve_client(api_key=api_key, base_url=base_url)
    transcript = client.audio.transcriptions.create(model=model, file=audio)
    return getattr(transcript, "text", str(transcript))


def transcribe_qa_samples(audios: Sequence, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = OPENAI_WHISPER_MODEL) -> List[str]:
    return [transcribe_qa_sample(audio, api_key=api_key, base_url=base_url, model=model) for audio in audios]


def transcribe_qa_segments(audio, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = OPENAI_WHISPER_MODEL) -> List[TranscriptSegment]:
    client = _resolve_client(api_key=api_key, base_url=base_url)
    transcript = client.audio.transcriptions.create(model=model, file=audio, response_format="verbose_json")
    segments = getattr(transcript, "segments", None) or []
    return [TranscriptSegment(text=getattr(segment, "text", ""), start=getattr(segment, "start", None), end=getattr(segment, "end", None)) for segment in segments]
