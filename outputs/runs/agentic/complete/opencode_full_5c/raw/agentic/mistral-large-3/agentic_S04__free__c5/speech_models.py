from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import timedelta


@dataclass
class WordInfo:
    word: str
    start_time: timedelta
    end_time: timedelta
    speaker_tag: Optional[int] = None


@dataclass
class SpeechSegment:
    text: str
    start_time: timedelta
    end_time: timedelta
    words: List[WordInfo] = None
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResult:
    segments: List[SpeechSegment]
    language_code: str
    audio_duration: timedelta


def normalize_response(response) -> TranscriptionResult:
    """Normalize Google Cloud Speech-to-Text response into a structured format."""
    segments = []

    for result in response.results:
        alternative = result.alternatives[0]
        words = []

        if result.alternatives[0].words:
            for word_info in result.alternatives[0].words:
                words.append(
                    WordInfo(
                        word=word_info.word,
                        start_time=timedelta(
                            seconds=word_info.start_time.seconds,
                            microseconds=word_info.start_time.nanos // 1000,
                        ),
                        end_time=timedelta(
                            seconds=word_info.end_time.seconds,
                            microseconds=word_info.end_time.nanos // 1000,
                        ),
                        speaker_tag=word_info.speaker_tag
                        if hasattr(word_info, "speaker_tag")
                        else None,
                    )
                )

        segments.append(
            SpeechSegment(
                text=alternative.transcript,
                start_time=timedelta(
                    seconds=result.result_end_time.seconds,
                    microseconds=result.result_end_time.nanos // 1000,
                ),
                end_time=timedelta(
                    seconds=result.result_end_time.seconds,
                    microseconds=result.result_end_time.nanos // 1000,
                ),
                words=words,
            )
        )

    audio_duration = timedelta(
        seconds=response.total_billed_time.seconds,
        microseconds=response.total_billed_time.nanos // 1000,
    )

    return TranscriptionResult(
        segments=segments,
        language_code=response.results[0].language_code
        if response.results
        else "en-US",
        audio_duration=audio_duration,
    )
