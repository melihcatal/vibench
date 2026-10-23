from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingSpeechRequest:
    audio_content: Optional[bytes] = None
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    enable_automatic_punctuation: bool = True
    interim_results: bool = True


@dataclass
class StreamingSpeechAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass
class StreamingSpeechResult:
    alternatives: list[StreamingSpeechAlternative]
    is_final: bool
    stability: Optional[float] = None


@dataclass
class StreamingSpeechResponse:
    results: list[StreamingSpeechResult]
    raw: Optional[Dict[str, Any]] = None


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def normalize_request(request: Any) -> StreamingSpeechRequest:
    return StreamingSpeechRequest(
        audio_content=_get_attr(request, "audio_content", _get_attr(request, "audioContent", None)),
        language_code=_get_attr(request, "language_code", _get_attr(request, "languageCode", "en-US")),
        sample_rate_hertz=int(_get_attr(request, "sample_rate_hertz", _get_attr(request, "sampleRateHertz", 16000))),
        enable_automatic_punctuation=bool(_get_attr(request, "enable_automatic_punctuation", _get_attr(request, "enableAutomaticPunctuation", True))),
        interim_results=bool(_get_attr(request, "interim_results", _get_attr(request, "interimResults", True))),
    )


def normalize_response(response: Any) -> StreamingSpeechResponse:
    results = []
    for result in _get_attr(response, "results", []) or []:
        alternatives = []
        for alternative in _get_attr(result, "alternatives", []) or []:
            alternatives.append(
                StreamingSpeechAlternative(
                    transcript=str(_get_attr(alternative, "transcript", "") or ""),
                    confidence=_get_attr(alternative, "confidence", None),
                )
            )
        results.append(
            StreamingSpeechResult(
                alternatives=alternatives,
                is_final=bool(_get_attr(result, "is_final", _get_attr(result, "isFinal", False))),
                stability=_get_attr(result, "stability", None),
            )
        )
    return StreamingSpeechResponse(results=results, raw=response if isinstance(response, dict) else None)


def normalize_transcript_text(response: Any) -> str:
    normalized = normalize_response(response)
    transcripts = []
    for result in normalized.results:
        if result.alternatives:
            transcripts.append(result.alternatives[0].transcript)
    return " ".join(part for part in transcripts if part).strip()


def is_final_response(response: Any) -> bool:
    normalized = normalize_response(response)
    return any(result.is_final for result in normalized.results)
