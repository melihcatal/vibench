import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StreamingSpeechToTextRequest:
    language_code: str = os.getenv("TRANSCRIPTION_LANGUAGE", "en-US")
    sample_rate_hz: int = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    media_encoding: str = os.getenv("AUDIO_ENCODING", "pcm")
    vocabulary_name: Optional[str] = os.getenv("AWS_TRANSCRIBE_VOCABULARY")
    show_speaker_labels: bool = os.getenv("AWS_TRANSCRIBE_SPEAKER_LABELS", "false").lower() == "true"
    enable_partial_results_stabilization: bool = os.getenv("AWS_TRANSCRIBE_PARTIAL_RESULTS_STABILIZATION", "true").lower() == "true"
    partial_results_stability: str = os.getenv("AWS_TRANSCRIBE_PARTIAL_RESULTS_STABILITY", "high")


@dataclass
class StreamingSpeechToTextAlternative:
    transcript: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StreamingSpeechToTextResponse:
    text: str = ""
    is_final: bool = False
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    alternatives: List[StreamingSpeechToTextAlternative] = field(default_factory=list)


class StreamingSpeechToTextNormalizer:
    def __init__(self) -> None:
        self._final_segments: List[str] = []
        self._partial_text: str = ""

    def normalize_event(self, event: Dict[str, Any]) -> StreamingSpeechToTextResponse:
        transcript_event = event.get("TranscriptEvent")
        if not transcript_event:
            return StreamingSpeechToTextResponse(text=self.get_full_text())

        results = transcript_event.get("Transcript", {}).get("Results", [])
        if not results:
            return StreamingSpeechToTextResponse(text=self.get_full_text())

        latest = results[0]
        alternatives_raw = latest.get("Alternatives", [])
        alternatives = [
            StreamingSpeechToTextAlternative(
                transcript=alternative.get("Transcript", ""),
                items=alternative.get("Items", []),
            )
            for alternative in alternatives_raw
        ]
        transcript = alternatives[0].transcript if alternatives else ""
        is_final = not latest.get("IsPartial", True)

        if is_final:
            if transcript:
                self._final_segments.append(transcript)
            self._partial_text = ""
        else:
            self._partial_text = transcript

        return StreamingSpeechToTextResponse(
            text=self.get_full_text(),
            is_final=is_final,
            start_time=latest.get("StartTime"),
            end_time=latest.get("EndTime"),
            alternatives=alternatives,
        )

    def get_full_text(self) -> str:
        parts = list(self._final_segments)
        if self._partial_text:
            parts.append(self._partial_text)
        return " ".join(parts).strip()


def build_streaming_speech_to_text_request(config: Optional[StreamingSpeechToTextRequest] = None) -> Dict[str, Any]:
    cfg = config or StreamingSpeechToTextRequest()
    request: Dict[str, Any] = {
        "LanguageCode": cfg.language_code,
        "MediaSampleRateHertz": cfg.sample_rate_hz,
        "MediaEncoding": cfg.media_encoding,
        "EnablePartialResultsStabilization": cfg.enable_partial_results_stabilization,
        "PartialResultsStability": cfg.partial_results_stability,
    }
    if cfg.vocabulary_name:
        request["VocabularyName"] = cfg.vocabulary_name
    if cfg.show_speaker_labels:
        request["ShowSpeakerLabels"] = True
    return request


def normalize_streaming_speech_to_text_event(event: Dict[str, Any], normalizer: Optional[StreamingSpeechToTextNormalizer] = None) -> StreamingSpeechToTextResponse:
    handler = normalizer or StreamingSpeechToTextNormalizer()
    return handler.normalize_event(event)
