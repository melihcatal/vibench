from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass
class SpeechJobRequest:
    audio_url: str
    speaker_labels: bool = False
    word_boost: list[str] = field(default_factory=list)


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptArtifact:
    transcript: str
    status: str = "completed"
    audio_url: Optional[str] = None
    segments: list[TranscriptSegment] = field(default_factory=list)
    raw: Any = None

    @classmethod
    def from_assemblyai(cls, result: Any) -> "TranscriptArtifact":
        segments: list[TranscriptSegment] = []
        utterances = getattr(result, "utterances", None) or []
        if utterances:
            for item in utterances:
                segments.append(
                    TranscriptSegment(
                        text=getattr(item, "text", ""),
                        start=getattr(item, "start", None),
                        end=getattr(item, "end", None),
                        speaker=getattr(item, "speaker", None),
                    )
                )
        else:
            paragraphs = getattr(result, "paragraphs", None)
            if paragraphs and getattr(paragraphs, "paragraphs", None):
                for item in paragraphs.paragraphs:
                    segments.append(
                        TranscriptSegment(
                            text=getattr(item, "text", ""),
                            start=getattr(item, "start", None),
                            end=getattr(item, "end", None),
                        )
                    )
        return cls(
            transcript=getattr(result, "text", "") or "",
            status=str(getattr(result, "status", "completed")),
            audio_url=getattr(result, "audio_url", None),
            segments=segments,
            raw=result,
        )


def join_segments(segments: Iterable[TranscriptSegment]) -> str:
    return " ".join(segment.text.strip() for segment in segments if segment.text).strip()
