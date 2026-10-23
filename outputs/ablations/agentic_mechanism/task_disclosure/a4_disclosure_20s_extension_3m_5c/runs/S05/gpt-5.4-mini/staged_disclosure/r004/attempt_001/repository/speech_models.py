from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Union


@dataclass(slots=True)
class StreamingSpeechToTextRequest:
    audio: Union[bytes, bytearray, memoryview]
    content_type: str = "audio/webm"
    language: Optional[str] = None
    model: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    enable_punctuation: bool = True
    interim_results: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SpeechToTextWord:
    word: str
    start: Optional[float] = None
    end: Optional[float] = None
    confidence: Optional[float] = None


@dataclass(slots=True)
class SpeechToTextAlternative:
    transcript: str
    confidence: Optional[float] = None
    words: List[SpeechToTextWord] = field(default_factory=list)


@dataclass(slots=True)
class StreamingSpeechToTextResponse:
    transcript: str
    is_final: bool = False
    confidence: Optional[float] = None
    alternatives: List[SpeechToTextAlternative] = field(default_factory=list)
    language: Optional[str] = None
    request_id: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def _to_bytes(audio: Union[bytes, bytearray, memoryview]) -> bytes:
    if isinstance(audio, bytes):
        return audio
    if isinstance(audio, bytearray):
        return bytes(audio)
    if isinstance(audio, memoryview):
        return audio.tobytes()
    raise TypeError("audio must be bytes-like")


def normalize_request(request: Union[StreamingSpeechToTextRequest, Dict[str, Any]]) -> StreamingSpeechToTextRequest:
    if isinstance(request, StreamingSpeechToTextRequest):
        return StreamingSpeechToTextRequest(
            audio=_to_bytes(request.audio),
            content_type=request.content_type,
            language=request.language,
            model=request.model,
            sample_rate_hz=request.sample_rate_hz,
            enable_punctuation=request.enable_punctuation,
            interim_results=request.interim_results,
            metadata=dict(request.metadata),
        )
    if isinstance(request, dict):
        audio = request.get("audio", b"")
        return StreamingSpeechToTextRequest(
            audio=_to_bytes(audio),
            content_type=request.get("content_type", "audio/webm"),
            language=request.get("language"),
            model=request.get("model"),
            sample_rate_hz=request.get("sample_rate_hz"),
            enable_punctuation=bool(request.get("enable_punctuation", True)),
            interim_results=bool(request.get("interim_results", True)),
            metadata=dict(request.get("metadata", {})),
        )
    raise TypeError("request must be a StreamingSpeechToTextRequest or dict")


def normalize_word(word: Union[SpeechToTextWord, Dict[str, Any], str]) -> SpeechToTextWord:
    if isinstance(word, SpeechToTextWord):
        return SpeechToTextWord(word=word.word, start=word.start, end=word.end, confidence=word.confidence)
    if isinstance(word, str):
        return SpeechToTextWord(word=word)
    if isinstance(word, dict):
        return SpeechToTextWord(
            word=str(word.get("word", "")),
            start=word.get("start"),
            end=word.get("end"),
            confidence=word.get("confidence"),
        )
    raise TypeError("word must be a SpeechToTextWord, dict, or str")


def normalize_alternative(alternative: Union[SpeechToTextAlternative, Dict[str, Any], str]) -> SpeechToTextAlternative:
    if isinstance(alternative, SpeechToTextAlternative):
        return SpeechToTextAlternative(
            transcript=alternative.transcript,
            confidence=alternative.confidence,
            words=[normalize_word(word) for word in alternative.words],
        )
    if isinstance(alternative, str):
        return SpeechToTextAlternative(transcript=alternative)
    if isinstance(alternative, dict):
        words = alternative.get("words", [])
        return SpeechToTextAlternative(
            transcript=str(alternative.get("transcript", "")),
            confidence=alternative.get("confidence"),
            words=[normalize_word(word) for word in words if word is not None],
        )
    raise TypeError("alternative must be a SpeechToTextAlternative, dict, or str")


def normalize_response(response: Union[StreamingSpeechToTextResponse, Dict[str, Any], str]) -> StreamingSpeechToTextResponse:
    if isinstance(response, StreamingSpeechToTextResponse):
        return StreamingSpeechToTextResponse(
            transcript=response.transcript,
            is_final=bool(response.is_final),
            confidence=response.confidence,
            alternatives=[normalize_alternative(alt) for alt in response.alternatives],
            language=response.language,
            request_id=response.request_id,
            raw=dict(response.raw),
        )
    if isinstance(response, str):
        return StreamingSpeechToTextResponse(transcript=response, raw={"transcript": response})
    if isinstance(response, dict):
        alternatives = response.get("alternatives", [])
        transcript = str(response.get("transcript", ""))
        if not transcript and alternatives:
            transcript = str(alternatives[0].get("transcript", "")) if isinstance(alternatives[0], dict) else str(alternatives[0])
        return StreamingSpeechToTextResponse(
            transcript=transcript,
            is_final=bool(response.get("is_final", response.get("final", False))),
            confidence=response.get("confidence"),
            alternatives=[normalize_alternative(alt) for alt in alternatives if alt is not None],
            language=response.get("language"),
            request_id=response.get("request_id") or response.get("id"),
            raw=dict(response),
        )
    raise TypeError("response must be a StreamingSpeechToTextResponse, dict, or str")


def normalize_stream_responses(responses: Iterable[Union[StreamingSpeechToTextResponse, Dict[str, Any], str]]) -> List[StreamingSpeechToTextResponse]:
    return [normalize_response(response) for response in responses]
