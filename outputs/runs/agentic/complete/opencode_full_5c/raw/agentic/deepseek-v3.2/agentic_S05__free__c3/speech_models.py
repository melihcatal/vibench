from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class SpeechRecognitionRequest:
    audio_content: bytes
    language_code: str = "en-US"
    sample_rate: int = 16000
    enable_punctuation: bool = True
    enable_word_confidence: bool = True
    enable_word_time_offsets: bool = True
    model: str = "default"
    use_enhanced: bool = False
    audio_channel_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class WordInfo:
    word: str
    confidence: Optional[float] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SpeechRecognitionResult:
    transcript: str
    confidence: Optional[float] = None
    is_final: bool = False
    language_code: str = "en-US"
    words: List[WordInfo] = None
    stability: Optional[float] = None
    result_end_time: Optional[float] = None
    alternatives: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.words is None:
            self.words = []
        if self.alternatives is None:
            self.alternatives = []

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["words"] = [word.to_dict() for word in self.words]
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_word_count(self) -> int:
        return len(self.words)

    def get_average_confidence(self) -> Optional[float]:
        if not self.words:
            return self.confidence

        confidences = [w.confidence for w in self.words if w.confidence is not None]
        if not confidences:
            return None

        return sum(confidences) / len(confidences)


@dataclass
class StreamingRecognitionEvent:
    results: List[SpeechRecognitionResult]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "results": [result.to_dict() for result in self.results],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def get_latest_transcript(self) -> str:
        if not self.results:
            return ""
        return self.results[-1].transcript

    def has_final_results(self) -> bool:
        return any(result.is_final for result in self.results)


class SpeechResponseNormalizer:
    @staticmethod
    def normalize_google_response(google_result) -> SpeechRecognitionResult:
        if not google_result.alternatives:
            return None

        main_alternative = google_result.alternatives[0]

        words = []
        if hasattr(main_alternative, "words") and main_alternative.words:
            for word in main_alternative.words:
                words.append(
                    WordInfo(
                        word=word.word,
                        confidence=word.confidence,
                        start_time=word.start_time.total_seconds()
                        if word.start_time
                        else None,
                        end_time=word.end_time.total_seconds()
                        if word.end_time
                        else None,
                    )
                )

        alternatives = []
        for alt in google_result.alternatives:
            alternatives.append(
                {"transcript": alt.transcript, "confidence": alt.confidence}
            )

        return SpeechRecognitionResult(
            transcript=main_alternative.transcript,
            confidence=main_alternative.confidence,
            is_final=google_result.is_final,
            language_code=getattr(google_result, "language_code", "en-US"),
            words=words,
            stability=getattr(google_result, "stability", None),
            result_end_time=google_result.result_end_time.total_seconds()
            if google_result.result_end_time
            else None,
            alternatives=alternatives,
        )

    @staticmethod
    def normalize_streaming_response(google_response) -> List[SpeechRecognitionResult]:
        results = []

        for result in google_response.results:
            normalized = SpeechResponseNormalizer.normalize_google_response(result)
            if normalized:
                results.append(normalized)

        return results


class SpeechRequestBuilder:
    @staticmethod
    def build_google_recognition_config(request: SpeechRecognitionRequest):
        from google.cloud import speech_v1p1beta1 as speech

        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=request.sample_rate,
            language_code=request.language_code,
            enable_automatic_punctuation=request.enable_punctuation,
            enable_word_confidence=request.enable_word_confidence,
            enable_word_time_offsets=request.enable_word_time_offsets,
            model=request.model,
            use_enhanced=request.use_enhanced,
            audio_channel_count=request.audio_channel_count,
        )

    @staticmethod
    def build_google_streaming_config(
        recognition_config, interim_results=True, single_utterance=False
    ):
        from google.cloud import speech_v1p1beta1 as speech

        return speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=interim_results,
            single_utterance=single_utterance,
        )
