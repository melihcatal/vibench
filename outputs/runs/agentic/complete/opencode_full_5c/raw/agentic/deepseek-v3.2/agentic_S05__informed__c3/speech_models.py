from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class SpeechRequest:
    audio_data: bytes
    language_code: str = "en-US"
    enable_punctuation: bool = True
    profanity_filter: bool = True
    word_level_timestamps: bool = False
    enable_dictation: bool = False
    custom_properties: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language_code": self.language_code,
            "enable_punctuation": self.enable_punctuation,
            "profanity_filter": self.profanity_filter,
            "word_level_timestamps": self.word_level_timestamps,
            "enable_dictation": self.enable_dictation,
            "audio_length_bytes": len(self.audio_data),
            "custom_properties": self.custom_properties or {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpeechRequest":
        return cls(
            audio_data=data.get("audio_data", b""),
            language_code=data.get("language_code", "en-US"),
            enable_punctuation=data.get("enable_punctuation", True),
            profanity_filter=data.get("profanity_filter", True),
            word_level_timestamps=data.get("word_level_timestamps", False),
            enable_dictation=data.get("enable_dictation", False),
            custom_properties=data.get("custom_properties"),
        )


@dataclass
class SpeechResult:
    text: str
    is_final: bool
    confidence: float
    language: str
    timestamp: datetime
    duration_seconds: Optional[float] = None
    offset_seconds: Optional[float] = None
    word_timestamps: Optional[List[Dict[str, Any]]] = None
    raw_result: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "text": self.text,
            "is_final": self.is_final,
            "confidence": self.confidence,
            "language": self.language,
            "timestamp": self.timestamp.isoformat(),
            "duration_seconds": self.duration_seconds,
            "offset_seconds": self.offset_seconds,
            "word_timestamps": self.word_timestamps,
        }
        if self.raw_result:
            result["raw_result"] = self.raw_result
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpeechResult":
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif timestamp is None:
            timestamp = datetime.now()

        return cls(
            text=data.get("text", ""),
            is_final=data.get("is_final", False),
            confidence=data.get("confidence", 0.0),
            language=data.get("language", "en-US"),
            timestamp=timestamp,
            duration_seconds=data.get("duration_seconds"),
            offset_seconds=data.get("offset_seconds"),
            word_timestamps=data.get("word_timestamps"),
            raw_result=data.get("raw_result"),
        )


@dataclass
class StreamingSession:
    session_id: str
    language_code: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_duration: Optional[float] = None
    final_results: List[SpeechResult] = None
    partial_results: List[SpeechResult] = None

    def __post_init__(self):
        if self.final_results is None:
            self.final_results = []
        if self.partial_results is None:
            self.partial_results = []

    def add_result(self, result: SpeechResult):
        if result.is_final:
            self.final_results.append(result)
        else:
            self.partial_results.append(result)

    def end_session(self):
        self.end_time = datetime.now()
        if self.start_time and self.end_time:
            self.total_duration = (self.end_time - self.start_time).total_seconds()

    def get_transcript(self, include_partial: bool = False) -> str:
        transcript = " ".join([r.text for r in self.final_results])
        if include_partial and self.partial_results:
            latest_partial = (
                self.partial_results[-1].text if self.partial_results else ""
            )
            if latest_partial:
                transcript += f" [{latest_partial}]"
        return transcript.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "language_code": self.language_code,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_duration": self.total_duration,
            "final_results_count": len(self.final_results),
            "partial_results_count": len(self.partial_results),
            "transcript": self.get_transcript(),
        }


class ResultNormalizer:
    @staticmethod
    def normalize_text(text: str, language: str = "en-US") -> str:
        text = text.strip()

        if language.startswith("en"):
            text = text.replace(" i ", " I ")
            if text and text[0].islower():
                text = text[0].upper() + text[1:]

        punctuation_map = {
            " ,": ",",
            " .": ".",
            " ?": "?",
            " !": "!",
            " :": ":",
            " ;": ";",
        }

        for wrong, correct in punctuation_map.items():
            text = text.replace(wrong, correct)

        return text

    @staticmethod
    def merge_partial_results(partials: List[SpeechResult]) -> str:
        if not partials:
            return ""

        merged = partials[0].text
        for i in range(1, len(partials)):
            current = partials[i].text
            prev = partials[i - 1].text

            if current.startswith(prev):
                merged = current
            elif len(current) > len(prev):
                overlap = ResultNormalizer._find_overlap(prev, current)
                if overlap:
                    merged = current
                else:
                    merged = current
            else:
                merged = current

        return merged

    @staticmethod
    def _find_overlap(text1: str, text2: str, min_overlap: int = 3) -> str:
        for i in range(min_overlap, len(text1) + 1):
            if text1[-i:] == text2[:i]:
                return text1[-i:]
        return ""

    @staticmethod
    def calculate_confidence_metrics(results: List[SpeechResult]) -> Dict[str, float]:
        if not results:
            return {"average": 0.0, "min": 0.0, "max": 0.0, "count": 0}

        finals = [r for r in results if r.is_final]
        if not finals:
            return {"average": 0.0, "min": 0.0, "max": 0.0, "count": 0}

        confidences = [r.confidence for r in finals]
        return {
            "average": sum(confidences) / len(confidences),
            "min": min(confidences),
            "max": max(confidences),
            "count": len(confidences),
        }


class SpeechResponseBuilder:
    @staticmethod
    def build_success_response(
        results: List[SpeechResult], session: Optional[StreamingSession] = None
    ) -> Dict[str, Any]:
        normalized_results = []
        for result in results:
            normalized_text = ResultNormalizer.normalize_text(
                result.text, result.language
            )
            normalized_results.append(
                {
                    "text": normalized_text,
                    "is_final": result.is_final,
                    "confidence": result.confidence,
                    "language": result.language,
                    "timestamp": result.timestamp.isoformat(),
                }
            )

        response = {
            "success": True,
            "results": normalized_results,
            "results_count": len(normalized_results),
            "final_results_count": len([r for r in results if r.is_final]),
            "confidence_metrics": ResultNormalizer.calculate_confidence_metrics(
                results
            ),
        }

        if session:
            response["session"] = session.to_dict()

        return response

    @staticmethod
    def build_error_response(
        error_message: str,
        error_code: Optional[str] = None,
        session: Optional[StreamingSession] = None,
    ) -> Dict[str, Any]:
        response = {"success": False, "error": error_message, "error_code": error_code}

        if session:
            response["session"] = session.to_dict()

        return response


class AudioChunkProcessor:
    @staticmethod
    def split_into_chunks(audio_data: bytes, chunk_size: int = 4096) -> List[bytes]:
        return [
            audio_data[i : i + chunk_size]
            for i in range(0, len(audio_data), chunk_size)
        ]

    @staticmethod
    def validate_audio_format(
        audio_data: bytes,
        sample_rate: int = 16000,
        channels: int = 1,
        bits_per_sample: int = 16,
    ) -> bool:
        if not audio_data:
            return False

        bytes_per_sample = bits_per_sample // 8
        expected_size_per_second = sample_rate * channels * bytes_per_sample

        if len(audio_data) > expected_size_per_second * 60:
            return False

        return len(audio_data) % (channels * bytes_per_sample) == 0

    @staticmethod
    def calculate_duration(
        audio_data: bytes,
        sample_rate: int = 16000,
        channels: int = 1,
        bits_per_sample: int = 16,
    ) -> float:
        bytes_per_sample = bits_per_sample // 8
        bytes_per_second = sample_rate * channels * bytes_per_sample

        if bytes_per_second == 0:
            return 0.0

        return len(audio_data) / bytes_per_second
