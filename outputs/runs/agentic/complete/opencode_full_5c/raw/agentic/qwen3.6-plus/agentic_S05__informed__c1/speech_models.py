from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class RecognitionResultType(str, Enum):
    INTERIM = "interim"
    FINAL = "final"


class SpeechEventType(str, Enum):
    TRANSCRIPT = "transcript"
    SPEECH_STARTED = "speech_started"
    SPEECH_ENDED = "speech_ended"
    VAD_TURN_START = "vad_turn_start"
    VAD_TURN_END = "vad_turn_end"
    METADATA = "metadata"


@dataclass
class WordInfo:
    word: str
    start: float
    end: float
    confidence: float = 0.0
    speaker: Optional[str] = None
    punctuated_word: Optional[str] = None


@dataclass
class StreamingRecognitionResult:
    text: str
    is_final: bool
    confidence: float = 0.0
    language_code: str = ""
    words: List[WordInfo] = field(default_factory=list)
    result_type: RecognitionResultType = RecognitionResultType.INTERIM
    channel_index: int = 0
    duration: float = 0.0
    segment_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_deepgram_response(cls, response: dict) -> "StreamingRecognitionResult":
        channel = response.get("channel", {})
        alternatives = channel.get("alternatives", [])
        if not alternatives:
            return cls(
                text="",
                is_final=False,
            )

        alt = alternatives[0]
        transcript = alt.get("transcript", "").strip()
        confidence = alt.get("confidence", 0.0)
        is_final = response.get("is_final", False)
        language = response.get("channel", {}).get("language", "")
        duration = response.get("duration", 0.0)

        words = []
        for w in alt.get("words", []):
            words.append(
                WordInfo(
                    word=w.get("word", ""),
                    start=w.get("start", 0.0),
                    end=w.get("end", 0.0),
                    confidence=w.get("confidence", 0.0),
                    punctuated_word=w.get("punctuated_word"),
                )
            )

        result_type = (
            RecognitionResultType.FINAL if is_final else RecognitionResultType.INTERIM
        )

        return cls(
            text=transcript,
            is_final=is_final,
            confidence=confidence,
            language_code=language,
            words=words,
            result_type=result_type,
            duration=duration,
            segment_id=response.get("speech_final", None),
        )


@dataclass
class StreamingSpeechEvent:
    event_type: SpeechEventType
    result: Optional[StreamingRecognitionResult] = None
    start_time: float = 0.0
    end_time: float = 0.0
    raw_payload: dict = field(default_factory=dict)

    @classmethod
    def from_deepgram_event(cls, raw: dict) -> "StreamingSpeechEvent":
        event_type_raw = raw.get("type", "")
        if event_type_raw == "Results":
            result = StreamingRecognitionResult.from_deepgram_response(raw)
            return cls(
                event_type=SpeechEventType.TRANSCRIPT,
                result=result,
                raw_payload=raw,
            )
        elif event_type_raw == "SpeechStarted":
            return cls(
                event_type=SpeechEventType.SPEECH_STARTED,
                start_time=raw.get("start", 0.0),
                raw_payload=raw,
            )
        elif event_type_raw == "UtteranceEnd":
            return cls(
                event_type=SpeechEventType.SPEECH_ENDED,
                end_time=raw.get("end", 0.0),
                raw_payload=raw,
            )
        elif event_type_raw == "Metadata":
            return cls(
                event_type=SpeechEventType.METADATA,
                raw_payload=raw,
            )
        return cls(
            event_type=SpeechEventType.TRANSCRIPT,
            raw_payload=raw,
        )


def normalize_transcript_text(result: StreamingRecognitionResult) -> str:
    text = result.text.strip()
    if not text:
        return ""
    if result.is_final:
        text = text[0].upper() + text[1:] if text else text
        if not text.endswith((".", "!", "?", ",", ";", ":")):
            text += "."
    return text


def build_streaming_request(
    language: str = "en-US",
    model: str = "nova-2",
    punctuate: bool = True,
    interim_results: bool = True,
    profanity_filter: bool = False,
    smart_format: bool = True,
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
    vad_events: bool = True,
    endpointing: Optional[int] = None,
    extra_options: Optional[dict] = None,
) -> dict:
    options = {
        "model": model,
        "language": language,
        "encoding": encoding,
        "sample_rate": sample_rate,
        "channels": channels,
        "punctuate": punctuate,
        "interim_results": interim_results,
        "smart_format": smart_format,
        "vad_events": vad_events,
    }
    if profanity_filter:
        options["profanity_filter"] = True
    if endpointing is not None:
        options["endpointing"] = endpointing
    if extra_options:
        options.update(extra_options)
    return options
