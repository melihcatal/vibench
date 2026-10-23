from __future__ import annotations

from typing import Any, Dict, List, Optional


class SpeechJobRequest:
    def __init__(
        self,
        audio_url: str,
        language_code: str = "en_us",
        speaker_labels: bool = False,
        speakers_expected: Optional[int] = None,
        webhook_url: Optional[str] = None,
    ) -> None:
        self.audio_url = audio_url
        self.language_code = language_code
        self.speaker_labels = speaker_labels
        self.speakers_expected = speakers_expected
        self.webhook_url = webhook_url

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
        }
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        if self.speaker_labels:
            payload["speaker_labels"] = True
            if self.speakers_expected is not None:
                payload["speakers_expected"] = self.speakers_expected
        return payload


class TranscriptSegment:
    def __init__(
        self,
        text: str,
        start_ms: Optional[int] = None,
        end_ms: Optional[int] = None,
        speaker: Optional[str] = None,
        confidence: Optional[float] = None,
    ) -> None:
        self.text = text
        self.start_ms = start_ms
        self.end_ms = end_ms
        self.speaker = speaker
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "speaker": self.speaker,
            "confidence": self.confidence,
        }


def normalize_utterances(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    utterances = result.get("utterances") or []
    normalized: List[Dict[str, Any]] = []
    for item in utterances:
        normalized.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
            ).to_dict()
        )
    return normalized


def normalize_words(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    words = result.get("words") or []
    normalized: List[Dict[str, Any]] = []
    for item in words:
        normalized.append(
            {
                "text": item.get("text") or item.get("word") or "",
                "start_ms": item.get("start"),
                "end_ms": item.get("end"),
                "confidence": item.get("confidence"),
                "speaker": item.get("speaker"),
            }
        )
    return normalized


def transcript_text(result: Dict[str, Any]) -> str:
    return (result.get("text") or "").strip()
