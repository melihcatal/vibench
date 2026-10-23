from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(frozen=True)
class SpeechRecognitionConfig:
    language_code: Optional[str] = None
    enable_automatic_punctuation: bool = False
    model: Optional[str] = None
    interim_results: bool = True

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"interim_results": self.interim_results}
        if self.language_code is not None:
            data["language_code"] = self.language_code
        if self.enable_automatic_punctuation:
            data["enable_automatic_punctuation"] = True
        if self.model is not None:
            data["model"] = self.model
        return data


@dataclass(frozen=True)
class SpeechRecognitionRequest:
    audio_content: bytes
    config: SpeechRecognitionConfig = field(default_factory=SpeechRecognitionConfig)

    def to_dict(self) -> Dict[str, Any]:
        return {"audio_content": self.audio_content, "config": self.config.to_dict()}


@dataclass(frozen=True)
class SpeechAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass(frozen=True)
class SpeechResult:
    alternatives: List[SpeechAlternative]
    is_final: bool = False
    stability: Optional[float] = None

    @property
    def transcript(self) -> str:
        return self.alternatives[0].transcript if self.alternatives else ""


@dataclass(frozen=True)
class SpeechResponse:
    results: List[SpeechResult] = field(default_factory=list)


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_results(results: Sequence[Mapping[str, Any] | SpeechResult]) -> List[SpeechResult]:
    normalized: List[SpeechResult] = []
    for result in results:
        if isinstance(result, SpeechResult):
            normalized.append(
                SpeechResult(
                    alternatives=[
                        SpeechAlternative(
                            transcript=normalize_transcript(alt.transcript),
                            confidence=alt.confidence,
                        )
                        for alt in result.alternatives
                    ],
                    is_final=result.is_final,
                    stability=result.stability,
                )
            )
            continue

        alternatives_data = result.get("alternatives", [])
        alternatives = [
            SpeechAlternative(
                transcript=normalize_transcript(str(alt.get("transcript", ""))),
                confidence=alt.get("confidence"),
            )
            for alt in alternatives_data
            if isinstance(alt, Mapping)
        ]
        normalized.append(
            SpeechResult(
                alternatives=alternatives,
                is_final=bool(result.get("is_final", False)),
                stability=result.get("stability"),
            )
        )
    return normalized


def response_from_dict(payload: Mapping[str, Any]) -> SpeechResponse:
    return SpeechResponse(results=normalize_results(payload.get("results", [])))
