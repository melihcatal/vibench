from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
import json


class AudioEncoding(str, Enum):
    LINEAR16 = "LINEAR16"
    FLAC = "FLAC"
    MULAW = "MULAW"
    AMR = "AMR"
    AMR_WB = "AMR_WB"
    OGG_OPUS = "OGG_OPUS"


class RecognitionModel(str, Enum):
    DEFAULT = "default"
    COMMAND_AND_SEARCH = "command_and_search"
    PHONE_CALL = "phone_call"
    VIDEO = "video"
    LATEST_LONG = "latest_long"


@dataclass
class RecognitionRequest:
    audio_content: bytes
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    enable_word_confidence: bool = True
    model: RecognitionModel = RecognitionModel.DEFAULT
    audio_channel_count: int = 1
    use_enhanced: bool = False

    def to_google_config(self):
        from google.cloud import speech

        encoding_map = {
            AudioEncoding.LINEAR16: speech.RecognitionConfig.AudioEncoding.LINEAR16,
            AudioEncoding.FLAC: speech.RecognitionConfig.AudioEncoding.FLAC,
            AudioEncoding.MULAW: speech.RecognitionConfig.AudioEncoding.MULAW,
            AudioEncoding.AMR: speech.RecognitionConfig.AudioEncoding.AMR,
            AudioEncoding.AMR_WB: speech.RecognitionConfig.AudioEncoding.AMR_WB,
            AudioEncoding.OGG_OPUS: speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        }

        model_map = {
            RecognitionModel.DEFAULT: "default",
            RecognitionModel.COMMAND_AND_SEARCH: "command_and_search",
            RecognitionModel.PHONE_CALL: "phone_call",
            RecognitionModel.VIDEO: "video",
            RecognitionModel.LATEST_LONG: "latest_long",
        }

        return speech.RecognitionConfig(
            encoding=encoding_map[self.encoding],
            sample_rate_hertz=self.sample_rate_hertz,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            enable_word_time_offsets=self.enable_word_time_offsets,
            enable_word_confidence=self.enable_word_confidence,
            model=model_map[self.model],
            audio_channel_count=self.audio_channel_count,
            use_enhanced=self.use_enhanced,
        )


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    confidence: float

    def to_dict(self):
        return {
            "word": self.word,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "confidence": self.confidence,
        }


@dataclass
class RecognitionResult:
    transcript: str
    confidence: float
    language_code: str
    is_final: bool
    words: List[WordInfo]
    alternatives: List[str]

    def to_dict(self):
        return {
            "transcript": self.transcript,
            "confidence": self.confidence,
            "language_code": self.language_code,
            "is_final": self.is_final,
            "words": [word.to_dict() for word in self.words],
            "alternatives": self.alternatives,
        }

    @classmethod
    def from_google_result(cls, google_result):
        from google.cloud import speech

        if not google_result.alternatives:
            return None

        alternative = google_result.alternatives[0]

        words = []
        if alternative.words:
            for word_info in alternative.words:
                words.append(
                    WordInfo(
                        word=word_info.word,
                        start_time=word_info.start_time.total_seconds(),
                        end_time=word_info.end_time.total_seconds(),
                        confidence=word_info.confidence,
                    )
                )

        alternatives = []
        if len(google_result.alternatives) > 1:
            alternatives = [alt.transcript for alt in google_result.alternatives[1:]]

        return cls(
            transcript=alternative.transcript,
            confidence=alternative.confidence or 0.0,
            language_code=google_result.language_code
            if hasattr(google_result, "language_code")
            else "en-US",
            is_final=google_result.is_final,
            words=words,
            alternatives=alternatives,
        )


@dataclass
class StreamingRecognitionResponse:
    results: List[RecognitionResult]
    total_billed_time: Optional[float] = None

    def to_dict(self):
        return {
            "results": [result.to_dict() for result in self.results],
            "total_billed_time": self.total_billed_time,
        }

    @classmethod
    def from_google_response(cls, google_response):
        results = []

        for result in google_response.results:
            recognition_result = RecognitionResult.from_google_result(result)
            if recognition_result:
                results.append(recognition_result)

        return cls(results=results)


class ResponseNormalizer:
    @staticmethod
    def normalize_transcript(transcript: str, add_punctuation: bool = True) -> str:
        transcript = transcript.strip()

        if add_punctuation and not transcript.endswith((".", "!", "?")):
            transcript += "."

        transcript = (
            transcript[0].upper() + transcript[1:] if transcript else transcript
        )

        return transcript

    @staticmethod
    def merge_partial_results(partial_results: List[RecognitionResult]) -> str:
        if not partial_results:
            return ""

        merged = []
        for result in partial_results:
            if result.is_final:
                merged.append(result.transcript)
            else:
                merged.append(f"[{result.transcript}]")

        return " ".join(merged)

    @staticmethod
    def extract_keywords(transcript: str, min_word_length: int = 4) -> List[str]:
        words = transcript.lower().split()
        keywords = []

        for word in words:
            word = word.strip(".,!?;:\"'()[]{}")
            if len(word) >= min_word_length and word.isalpha():
                keywords.append(word)

        return list(set(keywords))

    @staticmethod
    def calculate_speaking_rate(words: List[WordInfo], total_duration: float) -> float:
        if not words or total_duration <= 0:
            return 0.0

        return len(words) / total_duration * 60


def create_streaming_request(audio_chunk: bytes) -> Dict[str, Any]:
    return {
        "audio_content": audio_chunk,
        "encoding": "LINEAR16",
        "sample_rate": 16000,
    }


def parse_recognition_config(config_dict: Dict[str, Any]) -> RecognitionRequest:
    return RecognitionRequest(
        audio_content=b"",
        encoding=AudioEncoding(config_dict.get("encoding", "LINEAR16")),
        sample_rate_hertz=config_dict.get("sample_rate_hertz", 16000),
        language_code=config_dict.get("language_code", "en-US"),
        enable_automatic_punctuation=config_dict.get(
            "enable_automatic_punctuation", True
        ),
        enable_word_time_offsets=config_dict.get("enable_word_time_offsets", True),
        enable_word_confidence=config_dict.get("enable_word_confidence", True),
        model=RecognitionModel(config_dict.get("model", "default")),
        audio_channel_count=config_dict.get("audio_channel_count", 1),
        use_enhanced=config_dict.get("use_enhanced", False),
    )
