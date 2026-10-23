from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
import json


class AudioEncoding(Enum):
    LINEAR16 = "LINEAR16"
    FLAC = "FLAC"
    MULAW = "MULAW"
    AMR = "AMR"
    AMR_WB = "AMR_WB"
    OGG_OPUS = "OGG_OPUS"
    SPEEX_WITH_HEADER_BYTE = "SPEEX_WITH_HEADER_BYTE"


class RecognitionModel(Enum):
    LATEST_LONG = "latest_long"
    LATEST_SHORT = "latest_short"
    VIDEO = "video"
    PHONE_CALL = "phone_call"
    COMMAND_AND_SEARCH = "command_and_search"


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RecognitionAlternative:
    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[WordInfo]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        if self.words:
            result["words"] = [word.to_dict() for word in self.words]
        return result


@dataclass
class RecognitionResult:
    alternatives: List[RecognitionAlternative]
    is_final: bool
    stability: Optional[float] = None
    language_code: Optional[str] = None
    result_end_time: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["alternatives"] = [alt.to_dict() for alt in self.alternatives]
        return result

    @property
    def transcript(self) -> str:
        return self.alternatives[0].transcript if self.alternatives else ""


@dataclass
class StreamingRecognitionConfig:
    language_code: str = "en-US"
    sample_rate: int = 16000
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    enable_punctuation: bool = True
    enable_word_offsets: bool = True
    model: RecognitionModel = RecognitionModel.LATEST_LONG
    use_enhanced: bool = True
    speech_contexts: Optional[List[Dict[str, Any]]] = None

    def to_google_config(self):
        from google.cloud import speech_v1p1beta1 as speech

        config = speech.RecognitionConfig(
            encoding=getattr(
                speech.RecognitionConfig.AudioEncoding, self.encoding.value
            ),
            sample_rate_hertz=self.sample_rate,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_punctuation,
            enable_word_time_offsets=self.enable_word_offsets,
            model=self.model.value,
            use_enhanced=self.use_enhanced,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        if self.speech_contexts:
            streaming_config.speech_contexts = [
                speech.SpeechContext(
                    phrases=ctx.get("phrases", []), boost=ctx.get("boost", 0.0)
                )
                for ctx in self.speech_contexts
            ]

        return streaming_config


@dataclass
class StreamingRequest:
    audio_content: bytes
    config: StreamingRecognitionConfig

    def to_google_request(self):
        from google.cloud import speech_v1p1beta1 as speech

        return speech.StreamingRecognizeRequest(audio_content=self.audio_content)


class ResponseNormalizer:
    @staticmethod
    def normalize_google_response(google_result) -> RecognitionResult:
        if not google_result.alternatives:
            return RecognitionResult(alternatives=[], is_final=google_result.is_final)

        alternative = google_result.alternatives[0]

        words = None
        if alternative.words:
            words = [
                WordInfo(
                    word=word.word,
                    start_time=word.start_time.total_seconds(),
                    end_time=word.end_time.total_seconds(),
                    confidence=getattr(word, "confidence", None),
                )
                for word in alternative.words
            ]

        recognition_alternative = RecognitionAlternative(
            transcript=alternative.transcript,
            confidence=alternative.confidence,
            words=words,
        )

        return RecognitionResult(
            alternatives=[recognition_alternative],
            is_final=google_result.is_final,
            stability=getattr(google_result, "stability", None),
            language_code=getattr(google_result, "language_code", None),
            result_end_time=google_result.result_end_time.total_seconds()
            if hasattr(google_result, "result_end_time")
            else None,
        )

    @staticmethod
    def normalize_streaming_response(google_response) -> List[RecognitionResult]:
        normalized_results = []

        for result in google_response.results:
            normalized_result = ResponseNormalizer.normalize_google_response(result)
            normalized_results.append(normalized_result)

        return normalized_results

    @staticmethod
    def result_to_json(result: RecognitionResult) -> str:
        return json.dumps(result.to_dict(), indent=2)

    @staticmethod
    def combine_results(results: List[RecognitionResult]) -> str:
        final_transcripts = []
        for result in results:
            if result.is_final:
                final_transcripts.append(result.transcript)
        return " ".join(final_transcripts)


def create_speech_context(phrases: List[str], boost: float = 0.0) -> Dict[str, Any]:
    return {"phrases": phrases, "boost": boost}
