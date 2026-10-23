from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class StreamingSpeechRequest:
    model: str = "nova-2"
    language: str = "en"
    punctuate: bool = True
    interim_results: bool = True
    smart_format: bool = True
    encoding: str = "linear16"
    sample_rate: int = 16000
    channels: int = 1
    vad_events: bool = False
    utterance_end_ms: int = 1000

    def to_deepgram_options(self) -> dict:
        return {
            "model": self.model,
            "language": self.language,
            "punctuate": self.punctuate,
            "interim_results": self.interim_results,
            "smart_format": self.smart_format,
            "encoding": self.encoding,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "vad_events": self.vad_events,
            "utterance_end_ms": self.utterance_end_ms,
        }


@dataclass
class PartialTranscript:
    text: str
    is_final: bool = False
    confidence: float = 0.0
    language: str = "en"
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    words: List[dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class FinalTranscript:
    text: str
    confidence: float = 0.0
    language: str = "en"
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    words: List[dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StreamingSpeechResponse:
    partial: Optional[PartialTranscript] = None
    final: Optional[FinalTranscript] = None
    is_speech_final: bool = False
    duration: float = 0.0


def normalize_deepgram_result(result: dict) -> StreamingSpeechResponse:
    channel = result.get("channel", {}).get("alternatives", [{}])[0]
    text = channel.get("transcript", "").strip()
    confidence = channel.get("confidence", 0.0)
    language = result.get("channel", {}).get("language", "en")
    words = channel.get("words", [])

    start_time = None
    end_time = None
    if words:
        start_time = words[0].get("start")
        end_time = words[-1].get("end")

    is_final = result.get("is_final", False)
    speech_final = result.get("speech_final", False)
    duration = result.get("duration", 0.0)

    if is_final:
        final_transcript = FinalTranscript(
            text=text,
            confidence=confidence,
            language=language,
            start_time=start_time,
            end_time=end_time,
            words=words,
        )
        return StreamingSpeechResponse(
            final=final_transcript,
            is_speech_final=speech_final,
            duration=duration,
        )
    else:
        partial_transcript = PartialTranscript(
            text=text,
            is_final=False,
            confidence=confidence,
            language=language,
            start_time=start_time,
            end_time=end_time,
            words=words,
        )
        return StreamingSpeechResponse(
            partial=partial_transcript,
            is_speech_final=speech_final,
            duration=duration,
        )


def normalize_transcript_for_downstream(response: StreamingSpeechResponse) -> str:
    if response.final:
        return response.final.text
    elif response.partial:
        return response.partial.text
    return ""
