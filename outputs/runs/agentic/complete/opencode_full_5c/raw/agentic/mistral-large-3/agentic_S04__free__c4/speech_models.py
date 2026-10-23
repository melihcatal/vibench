from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import datetime


@dataclass
class WordInfo:
    word: str
    start_time: datetime.timedelta
    end_time: datetime.timedelta
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptSegment:
    text: str
    start_time: datetime.timedelta
    end_time: datetime.timedelta
    words: List[WordInfo] = None
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResult:
    segments: List[TranscriptSegment]
    language_code: str
    model: str


class SpeechNormalizer:
    @staticmethod
    def normalize_response(response: Any) -> TranscriptionResult:
        segments = []
        for result in response.results:
            for alternative in result.alternatives:
                words = []
                if alternative.words:
                    for word_info in alternative.words:
                        words.append(
                            WordInfo(
                                word=word_info.word,
                                start_time=datetime.timedelta(
                                    seconds=word_info.start_time.seconds,
                                    microseconds=word_info.start_time.nanos // 1000,
                                ),
                                end_time=datetime.timedelta(
                                    seconds=word_info.end_time.seconds,
                                    microseconds=word_info.end_time.nanos // 1000,
                                ),
                                speaker_tag=word_info.speaker_tag
                                if hasattr(word_info, "speaker_tag")
                                else None,
                            )
                        )

                segments.append(
                    TranscriptSegment(
                        text=alternative.transcript,
                        start_time=datetime.timedelta(
                            seconds=result.result_end_time.seconds,
                            microseconds=result.result_end_time.nanos // 1000,
                        )
                        if hasattr(result, "result_end_time")
                        else datetime.timedelta(0),
                        end_time=datetime.timedelta(
                            seconds=result.result_end_time.seconds,
                            microseconds=result.result_end_time.nanos // 1000,
                        )
                        if hasattr(result, "result_end_time")
                        else datetime.timedelta(0),
                        words=words,
                    )
                )

        return TranscriptionResult(
            segments=segments,
            language_code=response.language_code
            if hasattr(response, "language_code")
            else "en-US",
            model=response.model if hasattr(response, "model") else "latest_long",
        )
