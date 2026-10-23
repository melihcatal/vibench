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
    speaker_tag: Optional[int] = None
    words: Optional[List[WordInfo]] = None


@dataclass
class TranscriptionResult:
    transcript: str
    segments: List[SegmentInfo]
    words: List[WordInfo]
    language_code: str


class SpeechResponseParser:
    @staticmethod
    def parse_transcription_response(
        response: types.LongRunningRecognizeResponse,
    ) -> TranscriptionResult:
        transcript = ""
        segments = []
        words = []

        for result in response.results:
            alternative = result.alternatives[0]
            transcript += alternative.transcript + " "

            if result.alternatives[0].words:
                for word_info in result.alternatives[0].words:
                    words.append(
                        WordInfo(
                            word=word_info.word,
                            start_time=word_info.start_time.total_seconds(),
                            end_time=word_info.end_time.total_seconds(),
                            speaker_tag=word_info.speaker_tag
                            if hasattr(word_info, "speaker_tag")
                            else None,
                        )
                    )

            if hasattr(alternative, "words") and alternative.words:
                current_segment = None
                for word_info in alternative.words:
                    if word_info.speaker_tag is not None:
                        if (
                            current_segment is None
                            or current_segment.speaker_tag != word_info.speaker_tag
                        ):
                            if current_segment is not None:
                                segments.append(current_segment)
                            current_segment = SegmentInfo(
                                text="",
                                start_time=word_info.start_time.total_seconds(),
                                end_time=word_info.end_time.total_seconds(),
                                speaker_tag=word_info.speaker_tag,
                                words=[],
                            )
                        current_segment.text += word_info.word + " "
                        current_segment.end_time = word_info.end_time.total_seconds()
                        if current_segment.words is not None:
                            current_segment.words.append(
                                WordInfo(
                                    word=word_info.word,
                                    start_time=word_info.start_time.total_seconds(),
                                    end_time=word_info.end_time.total_seconds(),
                                    speaker_tag=word_info.speaker_tag,
                                )
                            )
                if current_segment is not None:
                    segments.append(current_segment)

        return TranscriptionResult(
            transcript=transcript.strip(),
            segments=segments,
            words=words,
            language_code=response.results[0].language_code
            if response.results
            else "en-US",
        )
