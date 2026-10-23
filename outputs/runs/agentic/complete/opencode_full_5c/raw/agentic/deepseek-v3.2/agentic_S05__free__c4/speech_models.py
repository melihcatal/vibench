from dataclasses import dataclass
from typing import Optional, List, Dict, Any
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
class RecognitionRequest:
    audio_content: bytes
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    sample_rate: int = 16000
    language_code: str = "en-US"
    enable_punctuation: bool = True
    model: RecognitionModel = RecognitionModel.LATEST_LONG
    speech_contexts: List[str] = None
    enable_word_confidence: bool = False
    enable_word_time_offsets: bool = False

    def __post_init__(self):
        if self.speech_contexts is None:
            self.speech_contexts = []


@dataclass
class StreamingRecognitionRequest:
    audio_chunks: List[bytes]
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    sample_rate: int = 16000
    language_code: str = "en-US"
    interim_results: bool = True
    single_utterance: bool = False


@dataclass
class RecognitionResult:
    transcript: str
    confidence: float
    is_final: bool
    language_code: str
    alternatives: List[Dict[str, Any]]

    @classmethod
    def from_google_result(cls, google_result, language_code: str = "en-US"):
        alternatives = []
        if google_result.alternatives:
            for alt in google_result.alternatives:
                alternatives.append(
                    {"transcript": alt.transcript, "confidence": alt.confidence}
                )

        primary_transcript = alternatives[0]["transcript"] if alternatives else ""
        primary_confidence = alternatives[0]["confidence"] if alternatives else 0.0

        return cls(
            transcript=primary_transcript,
            confidence=primary_confidence,
            is_final=google_result.is_final,
            language_code=language_code,
            alternatives=alternatives,
        )


@dataclass
class StreamingRecognitionResponse:
    results: List[RecognitionResult]
    total_billed_time: Optional[float] = None

    @classmethod
    def from_google_response(cls, google_response, language_code: str = "en-US"):
        results = []
        for result in google_response.results:
            if result.alternatives:
                recognition_result = RecognitionResult.from_google_result(
                    result, language_code
                )
                results.append(recognition_result)

        return cls(results=results)


class ResponseNormalizer:
    @staticmethod
    def normalize_transcript(transcript: str) -> str:
        transcript = transcript.strip()
        if transcript and not transcript.endswith((".", "!", "?")):
            transcript += "."
        return transcript

    @staticmethod
    def extract_keywords(transcript: str, min_length: int = 3) -> List[str]:
        words = transcript.lower().split()
        keywords = [
            word.strip(".,!?;:")
            for word in words
            if len(word.strip(".,!?;:")) >= min_length
        ]
        return list(set(keywords))

    @staticmethod
    def calculate_speech_rate(transcript: str, duration_seconds: float) -> float:
        word_count = len(transcript.split())
        if duration_seconds > 0:
            return word_count / duration_seconds
        return 0.0

    @staticmethod
    def merge_partial_results(partials: List[RecognitionResult]) -> str:
        transcripts = [result.transcript for result in partials if result.transcript]
        return " ".join(transcripts)


class RequestBuilder:
    @staticmethod
    def build_google_config(request: RecognitionRequest):
        from google.cloud import speech_v1p1beta1 as speech

        config = speech.RecognitionConfig(
            encoding=getattr(
                speech.RecognitionConfig.AudioEncoding, request.encoding.value
            ),
            sample_rate_hertz=request.sample_rate,
            language_code=request.language_code,
            enable_automatic_punctuation=request.enable_punctuation,
            model=request.model.value,
        )

        if request.speech_contexts:
            config.speech_contexts = [
                speech.SpeechContext(phrases=request.speech_contexts)
            ]

        if request.enable_word_confidence:
            config.enable_word_confidence = True

        if request.enable_word_time_offsets:
            config.enable_word_time_offsets = True

        return config

    @staticmethod
    def build_google_streaming_config(request: StreamingRecognitionRequest):
        from google.cloud import speech_v1p1beta1 as speech

        config = speech.RecognitionConfig(
            encoding=getattr(
                speech.RecognitionConfig.AudioEncoding, request.encoding.value
            ),
            sample_rate_hertz=request.sample_rate,
            language_code=request.language_code,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=request.interim_results,
            single_utterance=request.single_utterance,
        )

        return streaming_config
