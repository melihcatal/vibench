from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from google.cloud.speech_v1p1beta1 import types


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None


@dataclass
class SegmentInfo:
    text: str
    start_time: float
    end_time: float
    words: List[WordInfo]
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResult:
    transcript: str
    segments: List[SegmentInfo]
    words: List[WordInfo]
    language_code: str


class SpeechModels:
    @staticmethod
    def normalize_response(
        response: types.LongRunningRecognizeResponse,
    ) -> TranscriptionResult:
        transcript = ""
        segments = []
        words = []

        for result in response.results:
            alternative = result.alternatives[0]
            transcript += alternative.transcript + " "

            segment = SegmentInfo(
                text=alternative.transcript,
                start_time=result.result_end_time.total_seconds(),
                end_time=result.result_end_time.total_seconds(),
                words=[],
            )

            for word_info in alternative.words:
                word = WordInfo(
                    word=word_info.word,
                    start_time=word_info.start_time.total_seconds(),
                    end_time=word_info.end_time.total_seconds(),
                    speaker_tag=word_info.speaker_tag
                    if hasattr(word_info, "speaker_tag")
                    else None,
                )
                segment.words.append(word)
                words.append(word)

            segments.append(segment)

        return TranscriptionResult(
            transcript=transcript.strip(),
            segments=segments,
            words=words,
            language_code=response.results[0].language_code
            if response.results
            else "en-US",
        )
