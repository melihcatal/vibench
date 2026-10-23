from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import json
from datetime import datetime


class AudioEncoding(str, Enum):
    LINEAR16 = "LINEAR16"
    FLAC = "FLAC"
    MULAW = "MULAW"
    AMR = "AMR"
    AMR_WB = "AMR_WB"
    OGG_OPUS = "OGG_OPUS"
    SPEEX_WITH_HEADER_BYTE = "SPEEX_WITH_HEADER_BYTE"


class RecognitionModel(str, Enum):
    LATEST_LONG = "latest_long"
    LATEST_SHORT = "latest_short"
    VIDEO = "video"
    PHONE_CALL = "phone_call"
    COMMAND_AND_SEARCH = "command_and_search"
    DEFAULT = "default"


@dataclass
class RecognitionRequest:
    audio_data: bytes
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    enable_automatic_punctuation: bool = True
    model: RecognitionModel = RecognitionModel.LATEST_LONG
    use_enhanced: bool = False
    enable_word_time_offsets: bool = False
    enable_word_confidence: bool = False
    enable_speaker_diarization: bool = False
    diarization_speaker_count: int = 2
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language_code": self.language_code,
            "sample_rate_hertz": self.sample_rate_hertz,
            "encoding": self.encoding.value,
            "enable_automatic_punctuation": self.enable_automatic_punctuation,
            "model": self.model.value,
            "use_enhanced": self.use_enhanced,
            "enable_word_time_offsets": self.enable_word_time_offsets,
            "enable_word_confidence": self.enable_word_confidence,
            "enable_speaker_diarization": self.enable_speaker_diarization,
            "diarization_speaker_count": self.diarization_speaker_count,
            "audio_data_length": len(self.audio_data),
            "metadata": self.metadata or {},
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class WordInfo:
    word: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: Optional[float] = None
    speaker_tag: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "word": self.word,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "confidence": self.confidence,
            "speaker_tag": self.speaker_tag,
        }


@dataclass
class RecognitionResult:
    transcript: str
    confidence: Optional[float]
    language_code: str
    is_final: bool
    words: List[WordInfo]
    stability: Optional[float] = None
    result_end_time: Optional[float] = None
    speaker_tag: Optional[int] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "confidence": self.confidence,
            "language_code": self.language_code,
            "is_final": self.is_final,
            "words": [word.to_dict() for word in self.words],
            "stability": self.stability,
            "result_end_time": self.result_end_time,
            "speaker_tag": self.speaker_tag,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def duration(self) -> Optional[float]:
        if self.words:
            first_word = self.words[0]
            last_word = self.words[-1]
            if first_word.start_time is not None and last_word.end_time is not None:
                return last_word.end_time - first_word.start_time
        return None


@dataclass
class StreamingSession:
    session_id: str
    language_code: str
    start_time: datetime
    end_time: Optional[datetime] = None
    results: List[RecognitionResult] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.results is None:
            self.results = []
        if self.metadata is None:
            self.metadata = {}

    def add_result(self, result: RecognitionResult):
        self.results.append(result)

    def finalize(self):
        self.end_time = datetime.now()

    def get_final_transcript(self) -> str:
        final_results = [r for r in self.results if r.is_final]
        return " ".join([r.transcript for r in final_results])

    def get_average_confidence(self) -> float:
        confidences = [r.confidence for r in self.results if r.confidence is not None]
        if not confidences:
            return 0.0
        return sum(confidences) / len(confidences)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "language_code": self.language_code,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": (self.end_time - self.start_time).total_seconds()
            if self.end_time
            else None,
            "result_count": len(self.results),
            "final_transcript": self.get_final_transcript(),
            "average_confidence": self.get_average_confidence(),
            "metadata": self.metadata,
        }


class ResponseNormalizer:
    @staticmethod
    def normalize_google_response(
        google_result, language_code: str = "en-US"
    ) -> RecognitionResult:
        alternative = google_result.alternatives[0]

        words = []
        if hasattr(alternative, "words") and alternative.words:
            for word_info in alternative.words:
                word = WordInfo(
                    word=word_info.word,
                    start_time=word_info.start_time.total_seconds()
                    if hasattr(word_info, "start_time")
                    else None,
                    end_time=word_info.end_time.total_seconds()
                    if hasattr(word_info, "end_time")
                    else None,
                    confidence=word_info.confidence
                    if hasattr(word_info, "confidence")
                    else None,
                    speaker_tag=word_info.speaker_tag
                    if hasattr(word_info, "speaker_tag")
                    else None,
                )
                words.append(word)

        return RecognitionResult(
            transcript=alternative.transcript,
            confidence=alternative.confidence,
            language_code=language_code,
            is_final=google_result.is_final,
            words=words,
            stability=getattr(google_result, "stability", None),
            result_end_time=getattr(google_result, "result_end_time", None),
            speaker_tag=getattr(google_result, "speaker_tag", None),
        )

    @staticmethod
    def normalize_streaming_response(
        response_data: Dict[str, Any],
    ) -> RecognitionResult:
        return RecognitionResult(
            transcript=response_data.get("transcript", ""),
            confidence=response_data.get("confidence"),
            language_code=response_data.get("language_code", "en-US"),
            is_final=response_data.get("is_final", False),
            words=[
                WordInfo(
                    word=w.get("word", ""),
                    confidence=w.get("confidence"),
                    speaker_tag=w.get("speaker_tag"),
                )
                for w in response_data.get("words", [])
            ],
            stability=response_data.get("stability"),
            result_end_time=response_data.get("result_end_time"),
            speaker_tag=response_data.get("speaker_tag"),
        )


class TranscriptProcessor:
    @staticmethod
    def clean_transcript(transcript: str) -> str:
        import re

        transcript = transcript.strip()

        transcript = re.sub(r"\s+", " ", transcript)

        transcript = re.sub(r"\[.*?\]", "", transcript)

        transcript = re.sub(r"\(.*?\)", "", transcript)

        transcript = transcript.replace("  ", " ")

        return transcript.strip()

    @staticmethod
    def split_into_sentences(transcript: str) -> List[str]:
        import re

        sentence_endings = r"(?<=[.!?])\s+"
        sentences = re.split(sentence_endings, transcript)

        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def calculate_wer(reference: str, hypothesis: str) -> float:
        import numpy as np

        ref_words = reference.split()
        hyp_words = hypothesis.split()

        if not ref_words:
            return 0.0 if not hyp_words else 1.0

        d = np.zeros((len(ref_words) + 1, len(hyp_words) + 1))

        for i in range(len(ref_words) + 1):
            d[i][0] = i
        for j in range(len(hyp_words) + 1):
            d[0][j] = j

        for i in range(1, len(ref_words) + 1):
            for j in range(1, len(hyp_words) + 1):
                if ref_words[i - 1] == hyp_words[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    substitution = d[i - 1][j - 1] + 1
                    insertion = d[i][j - 1] + 1
                    deletion = d[i - 1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)

        wer = d[len(ref_words)][len(hyp_words)] / len(ref_words)
        return wer
