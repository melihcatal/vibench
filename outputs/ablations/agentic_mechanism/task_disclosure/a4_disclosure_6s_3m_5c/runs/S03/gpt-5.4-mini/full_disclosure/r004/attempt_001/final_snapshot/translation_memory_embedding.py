from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class TranslationMemorySegment:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    segment_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized_text(self) -> str:
        return " ".join(f"{self.source_text}\n{self.translated_text}".split())


@dataclass(frozen=True)
class TranslationMemoryEmbedding:
    segment: TranslationMemorySegment
    embedding: List[float]
    model: str


def build_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("TRANSLATION_API_KEY")
    if not key:
        raise ValueError("Missing API key: set OPENAI_API_KEY or TRANSLATION_API_KEY")
    kwargs: Dict[str, Any] = {"api_key": key}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    organization = os.getenv("OPENAI_ORGANIZATION")
    if organization:
        kwargs["organization"] = organization
    project = os.getenv("OPENAI_PROJECT")
    if project:
        kwargs["project"] = project
    return OpenAI(**kwargs)


def _embedding_input(segment: TranslationMemorySegment) -> str:
    parts = [segment.source_text.strip(), segment.translated_text.strip()]
    if segment.source_language:
        parts.append(f"source_language={segment.source_language.strip()}")
    if segment.target_language:
        parts.append(f"target_language={segment.target_language.strip()}")
    return "\n".join(part for part in parts if part)


def embed_translation_memory_segment(
    segment: Mapping[str, Any] | TranslationMemorySegment,
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> TranslationMemoryEmbedding:
    tm_segment = segment if isinstance(segment, TranslationMemorySegment) else TranslationMemorySegment(
        source_text=str(segment.get("source_text", "")),
        translated_text=str(segment.get("translated_text", "")),
        source_language=segment.get("source_language"),
        target_language=segment.get("target_language"),
        segment_id=segment.get("segment_id"),
        metadata=dict(segment.get("metadata", {}) or {}),
    )
    active_client = client or build_openai_client(api_key=api_key)
    response = active_client.embeddings.create(model=model, input=_embedding_input(tm_segment))
    return TranslationMemoryEmbedding(segment=tm_segment, embedding=list(response.data[0].embedding), model=model)


def embed_translation_memory_segments(
    segments: Sequence[Mapping[str, Any] | TranslationMemorySegment],
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> List[TranslationMemoryEmbedding]:
    active_client = client or build_openai_client(api_key=api_key)
    normalized_segments: List[TranslationMemorySegment] = []
    inputs: List[str] = []
    for segment in segments:
        tm_segment = segment if isinstance(segment, TranslationMemorySegment) else TranslationMemorySegment(
            source_text=str(segment.get("source_text", "")),
            translated_text=str(segment.get("translated_text", "")),
            source_language=segment.get("source_language"),
            target_language=segment.get("target_language"),
            segment_id=segment.get("segment_id"),
            metadata=dict(segment.get("metadata", {}) or {}),
        )
        normalized_segments.append(tm_segment)
        inputs.append(_embedding_input(tm_segment))
    response = active_client.embeddings.create(model=model, input=inputs)
    return [
        TranslationMemoryEmbedding(segment=segment, embedding=list(item.embedding), model=model)
        for segment, item in zip(normalized_segments, response.data)
    ]
