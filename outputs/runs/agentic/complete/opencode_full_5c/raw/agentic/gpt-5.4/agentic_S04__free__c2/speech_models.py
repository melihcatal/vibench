from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BatchTranscriptionRequest:
    audio_url: str
    language_code: str = "en_us"
    webhook_url: str | None = None
    enable_speaker_labels: bool = False
    speakers_expected: int | None = None

    def to_assemblyai_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
        }
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        if self.enable_speaker_labels:
            payload["speaker_labels"] = True
        if self.speakers_expected is not None:
            payload["speakers_expected"] = self.speakers_expected
        return payload


@dataclass(slots=True)
class TranscriptSegment:
    start_ms: int
    end_ms: int
    text: str
    speaker: str | None = None
    confidence: float | None = None
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class BatchTranscriptionResult:
    transcript_id: str
    status: str
    text: str = ""
    language_code: str | None = None
    audio_url: str | None = None
    segments: list[TranscriptSegment] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_segments(transcript_data: dict[str, Any]) -> list[TranscriptSegment]:
    utterances = transcript_data.get("utterances") or []
    if utterances:
        return [
            TranscriptSegment(
                start_ms=int(item.get("start", 0)),
                end_ms=int(item.get("end", 0)),
                text=str(item.get("text", "")).strip(),
                speaker=str(item.get("speaker"))
                if item.get("speaker") is not None
                else None,
                confidence=float(item["confidence"])
                if item.get("confidence") is not None
                else None,
                words=list(item.get("words") or []),
            )
            for item in utterances
        ]

    words = transcript_data.get("words") or []
    if words:
        segments: list[TranscriptSegment] = []
        current_words: list[dict[str, Any]] = []
        current_start = 0
        current_end = 0
        for item in words:
            if not current_words:
                current_start = int(item.get("start", 0))
            current_words.append(item)
            current_end = int(item.get("end", current_start))
            if len(current_words) >= 20 or str(item.get("text", "")).endswith(
                (".", "?", "!")
            ):
                text = " ".join(
                    str(word.get("text", "")).strip() for word in current_words
                ).strip()
                segments.append(
                    TranscriptSegment(
                        start_ms=current_start,
                        end_ms=current_end,
                        text=text,
                        confidence=None,
                        words=list(current_words),
                    )
                )
                current_words = []
        if current_words:
            text = " ".join(
                str(word.get("text", "")).strip() for word in current_words
            ).strip()
            segments.append(
                TranscriptSegment(
                    start_ms=current_start,
                    end_ms=current_end,
                    text=text,
                    confidence=None,
                    words=list(current_words),
                )
            )
        return segments

    text = str(transcript_data.get("text", "")).strip()
    if not text:
        return []
    return [
        TranscriptSegment(
            start_ms=0,
            end_ms=int(transcript_data.get("audio_duration", 0)),
            text=text,
        )
    ]


def normalize_transcription_result(
    transcript_data: dict[str, Any],
) -> BatchTranscriptionResult:
    return BatchTranscriptionResult(
        transcript_id=str(transcript_data.get("id", "")),
        status=str(transcript_data.get("status", "queued")),
        text=str(transcript_data.get("text", "")),
        language_code=transcript_data.get("language_code"),
        audio_url=transcript_data.get("audio_url"),
        segments=normalize_segments(transcript_data),
        raw=transcript_data,
    )
