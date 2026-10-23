from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import timedelta


@dataclass
class WordInfo:
    word: str
    start_offset: timedelta
    end_offset: timedelta
    speaker_tag: Optional[int] = None


@dataclass
class SegmentInfo:
    text: str
    start_offset: timedelta
    end_offset: timedelta
    words: List[WordInfo]
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResult:
    segments: List[SegmentInfo]
    language_code: str
    audio_duration: timedelta


@dataclass
class DiarizationResult:
    segments: List[SegmentInfo]
    speaker_labels: Dict[int, str]


class SpeechNormalizer:
    @staticmethod
    def normalize_response(response) -> TranscriptionResult:
        segments = []
        for result in response.results:
            for alternative in result.alternatives:
                words = []
                for word_info in alternative.words:
                    words.append(
                        WordInfo(
                            word=word_info.word,
                            start_offset=timedelta(
                                seconds=word_info.start_offset.seconds,
                                microseconds=word_info.start_offset.microseconds,
                            ),
                            end_offset=timedelta(
                                seconds=word_info.end_offset.seconds,
                                microseconds=word_info.end_offset.microseconds,
                            ),
                            speaker_tag=word_info.speaker_tag
                            if hasattr(word_info, "speaker_tag")
                            else None,
                        )
                    )

                segments.append(
                    SegmentInfo(
                        text=alternative.transcript,
                        start_offset=timedelta(
                            seconds=result.result_end_offset.seconds,
                            microseconds=result.result_end_offset.microseconds,
                        )
                        - timedelta(seconds=len(alternative.transcript) / 15),
                        end_offset=timedelta(
                            seconds=result.result_end_offset.seconds,
                            microseconds=result.result_end_offset.microseconds,
                        ),
                        words=words,
                        speaker_tag=words[0].speaker_tag
                        if words and hasattr(words[0], "speaker_tag")
                        else None,
                    )
                )

        return TranscriptionResult(
            segments=segments,
            language_code=response.language_code,
            audio_duration=timedelta(
                seconds=response.audio_duration.seconds,
                microseconds=response.audio_duration.microseconds,
            ),
        )

    @staticmethod
    def normalize_diarization(response) -> DiarizationResult:
        transcription_result = SpeechNormalizer.normalize_response(response)
        speaker_labels = {}
        for segment in transcription_result.segments:
            if (
                segment.speaker_tag is not None
                and segment.speaker_tag not in speaker_labels
            ):
                speaker_labels[segment.speaker_tag] = f"Speaker {segment.speaker_tag}"

        return DiarizationResult(
            segments=transcription_result.segments, speaker_labels=speaker_labels
        )
