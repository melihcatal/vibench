from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptJobRequest:
    audio_url: str
    language_code: Optional[str] = None
    diarization: bool = False
    timestamps: bool = False

    def to_payload(self) -> Dict[str, Any]:
        payload = {"audio_url": self.audio_url}
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.diarization:
            payload["speaker_labels"] = True
        if self.timestamps:
            payload["auto_chapters"] = False
            payload["word_boost"] = []
        return payload


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[float] = None
    end: Optional[float] = None
    speaker: Optional[str] = None


def normalize_transcript(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("text") or payload.get("transcript") or ""
    segments: List[Dict[str, Any]] = []
    for item in payload.get("utterances", payload.get("segments", [])):
        segments.append(
            {
                "text": item.get("text", ""),
                "start": item.get("start"),
                "end": item.get("end"),
                "speaker": item.get("speaker"),
            }
        )
    words = payload.get("words", [])
    return {"text": text, "segments": segments, "words": words, "raw": payload}
