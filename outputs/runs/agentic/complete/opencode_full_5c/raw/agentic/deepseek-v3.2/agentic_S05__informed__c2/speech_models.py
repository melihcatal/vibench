from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    result_id: Optional[str] = None
    offset: Optional[int] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    confidence: Optional[float] = None
    speaker_id: Optional[str] = None
    timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_final": self.is_final,
            "result_id": self.result_id,
            "offset": self.offset,
            "duration": self.duration,
            "language": self.language,
            "confidence": self.confidence,
            "speaker_id": self.speaker_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpeechRecognitionResult":
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None

        return cls(
            text=data["text"],
            is_final=data["is_final"],
            result_id=data.get("result_id"),
            offset=data.get("offset"),
            duration=data.get("duration"),
            language=data.get("language"),
            confidence=data.get("confidence"),
            speaker_id=data.get("speaker_id"),
            timestamp=timestamp,
        )


@dataclass
class StreamingRequest:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    enable_word_timestamps: bool = True
    profanity_filter: str = "masked"
    enable_speaker_diarization: bool = False
    max_alternatives: int = 1

    def to_config_dict(self) -> Dict[str, Any]:
        return {
            "language_code": self.language_code,
            "enable_punctuation": self.enable_punctuation,
            "enable_word_timestamps": self.enable_word_timestamps,
            "profanity_filter": self.profanity_filter,
            "enable_speaker_diarization": self.enable_speaker_diarization,
            "max_alternatives": self.max_alternatives,
        }


@dataclass
class StreamingResponse:
    results: List[SpeechRecognitionResult]
    session_id: Optional[str] = None
    error: Optional[str] = None

    def add_result(self, result: SpeechRecognitionResult):
        self.results.append(result)

    def get_final_results(self) -> List[SpeechRecognitionResult]:
        return [r for r in self.results if r.is_final]

    def get_interim_results(self) -> List[SpeechRecognitionResult]:
        return [r for r in self.results if not r.is_final]

    def get_latest_interim(self) -> Optional[SpeechRecognitionResult]:
        interim = self.get_interim_results()
        return interim[-1] if interim else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "session_id": self.session_id,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamingResponse":
        results = [
            SpeechRecognitionResult.from_dict(r) for r in data.get("results", [])
        ]
        return cls(
            results=results, session_id=data.get("session_id"), error=data.get("error")
        )


class ResultNormalizer:
    @staticmethod
    def normalize_text(text: str, add_punctuation: bool = True) -> str:
        if not text:
            return text

        text = text.strip()

        if (
            add_punctuation
            and text
            and not text.endswith((".", "!", "?", ",", ";", ":"))
        ):
            if text.lower().startswith(("who", "what", "where", "when", "why", "how")):
                text = text + "?"
            else:
                text = text + "."

        text = text[0].upper() + text[1:] if text else text

        return text

    @staticmethod
    def extract_confidence(azure_result: Any) -> Optional[float]:
        if hasattr(azure_result, "confidence"):
            confidence_value = azure_result.confidence
            if confidence_value == speechsdk.Confidence.High:
                return 0.9
            elif confidence_value == speechsdk.Confidence.Normal:
                return 0.7
            elif confidence_value == speechsdk.Confidence.Low:
                return 0.4
        return None

    @staticmethod
    def create_from_azure_event(
        event: Any, is_final: bool = False
    ) -> SpeechRecognitionResult:
        from datetime import datetime

        text = event.result.text if hasattr(event.result, "text") else ""

        result = SpeechRecognitionResult(
            text=text,
            is_final=is_final,
            result_id=event.result.result_id
            if hasattr(event.result, "result_id")
            else None,
            offset=event.result.offset if hasattr(event.result, "offset") else None,
            duration=event.result.duration.total_seconds()
            if hasattr(event.result, "duration")
            else None,
            timestamp=datetime.now(),
        )

        confidence = ResultNormalizer.extract_confidence(event.result)
        if confidence:
            result.confidence = confidence

        return result


class TranscriptAggregator:
    def __init__(self):
        self.final_transcript = ""
        self.interim_buffer = ""
        self.results_history = []

    def add_result(self, result: SpeechRecognitionResult):
        self.results_history.append(result)

        if result.is_final:
            normalized = ResultNormalizer.normalize_text(result.text)
            if self.final_transcript:
                self.final_transcript += " " + normalized
            else:
                self.final_transcript = normalized
            self.interim_buffer = ""
        else:
            self.interim_buffer = result.text

    def get_full_transcript(self) -> str:
        return self.final_transcript

    def get_current_view(self) -> str:
        if self.interim_buffer:
            return (
                self.final_transcript + " " + self.interim_buffer
                if self.final_transcript
                else self.interim_buffer
            )
        return self.final_transcript

    def clear(self):
        self.final_transcript = ""
        self.interim_buffer = ""
        self.results_history = []

    def export_json(self) -> str:
        data = {
            "final_transcript": self.final_transcript,
            "results": [r.to_dict() for r in self.results_history],
            "timestamp": datetime.now().isoformat(),
        }
        return json.dumps(data, indent=2)
