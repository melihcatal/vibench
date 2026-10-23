from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TranscriptionRequest:
    audio_data: bytes
    sample_rate: int = 16000
    channels: int = 1
    language: str = "en-US"
    enable_punctuation: bool = True
    enable_smart_format: bool = True
    model: str = "nova-2"

    def to_deepgram_options(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "language": self.language,
            "punctuate": self.enable_punctuation,
            "smart_format": self.enable_smart_format,
            "encoding": "linear16",
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "interim_results": True,
        }


@dataclass
class TranscriptionResult:
    transcript: str
    is_final: bool
    confidence: Optional[float] = None
    words: Optional[List[Dict[str, Any]]] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    speaker: Optional[int] = None

    @classmethod
    def from_deepgram_response(
        cls, response: Dict[str, Any]
    ) -> Optional["TranscriptionResult"]:
        if "channel" not in response:
            return None

        channel = response["channel"]
        alternatives = channel.get("alternatives", [])
        if not alternatives:
            return None

        alternative = alternatives[0]
        transcript = alternative.get("transcript", "")
        if not transcript:
            return None

        words = alternative.get("words", [])
        confidence = alternative.get("confidence")

        start_time = None
        end_time = None
        if words:
            start_time = words[0].get("start")
            end_time = words[-1].get("end")

        return cls(
            transcript=transcript,
            is_final=response.get("is_final", False),
            confidence=confidence,
            words=words,
            start_time=start_time,
            end_time=end_time,
            speaker=channel.get("speaker"),
        )


@dataclass
class StreamingSession:
    session_id: str
    start_time: datetime
    language: str
    model: str
    is_active: bool = True
    partial_transcript: str = ""
    final_transcripts: List[str] = None

    def __post_init__(self):
        if self.final_transcripts is None:
            self.final_transcripts = []

    def add_partial(self, text: str):
        self.partial_transcript = text

    def add_final(self, text: str):
        self.final_transcripts.append(text)
        self.partial_transcript = ""

    def get_full_transcript(self) -> str:
        return " ".join(self.final_transcripts)


class TranscriptNormalizer:
    @staticmethod
    def normalize_punctuation(text: str) -> str:
        text = text.strip()
        if not text:
            return text

        if text[-1] not in ".!?":
            text += "."

        text = text[0].upper() + text[1:]
        return text

    @staticmethod
    def remove_fillers(text: str) -> str:
        fillers = ["um", "uh", "ah", "er", "like", "you know", "i mean"]
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in fillers]
        return " ".join(filtered_words)

    @staticmethod
    def normalize_spacing(text: str) -> str:
        import re

        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s([.,!?;:])", r"\1", text)
        text = re.sub(r"([.,!?;:])\s", r"\1 ", text)
        return text.strip()

    @staticmethod
    def normalize_transcript(transcript: str, remove_fillers: bool = True) -> str:
        text = transcript.strip()
        if remove_fillers:
            text = TranscriptNormalizer.remove_fillers(text)
        text = TranscriptNormalizer.normalize_spacing(text)
        text = TranscriptNormalizer.normalize_punctuation(text)
        return text


class ResponseParser:
    @staticmethod
    def parse_streaming_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        event_type = event.get("type", "unknown")

        if event_type == "Results":
            return ResponseParser._parse_results_event(event)
        elif event_type == "Metadata":
            return {"type": "metadata", "data": event}
        elif event_type == "Error":
            return {"type": "error", "error": event.get("description", "Unknown error")}

        return None

    @staticmethod
    def _parse_results_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if "channel" not in event:
            return None

        channel = event["channel"]
        alternatives = channel.get("alternatives", [])
        if not alternatives:
            return None

        alternative = alternatives[0]
        transcript = alternative.get("transcript", "")
        if not transcript:
            return None

        return {
            "type": "transcript",
            "transcript": transcript,
            "is_final": event.get("is_final", False),
            "confidence": alternative.get("confidence"),
            "words": alternative.get("words", []),
            "speaker": channel.get("speaker"),
            "speech_final": event.get("speech_final", False),
        }

    @staticmethod
    def extract_words_with_timing(event: Dict[str, Any]) -> List[Dict[str, Any]]:
        if "channel" not in event:
            return []

        channel = event["channel"]
        alternatives = channel.get("alternatives", [])
        if not alternatives:
            return []

        alternative = alternatives[0]
        words = alternative.get("words", [])

        parsed_words = []
        for word_info in words:
            parsed_words.append(
                {
                    "word": word_info.get("word", ""),
                    "start": word_info.get("start"),
                    "end": word_info.get("end"),
                    "confidence": word_info.get("confidence"),
                    "speaker": channel.get("speaker"),
                }
            )

        return parsed_words
