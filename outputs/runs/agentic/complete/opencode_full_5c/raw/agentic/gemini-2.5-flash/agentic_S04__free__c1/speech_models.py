from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TranscriptionRequest:
    gcs_uri: str
    sample_rate_hertz: int
    language_code: str
    enable_diarization: bool = False
    diarization_speaker_count: Optional[int] = None
    enable_word_time_offsets: bool = False


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None


@dataclass
class SegmentInfo:
    transcript: str
    words: List[WordInfo]
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResponse:
    segments: List[SegmentInfo]
    full_transcript: str


def normalize_speech_response(response) -> TranscriptionResponse:
    """Normalizes the Google Cloud Speech-to-Text API response."""
    full_transcript = ""
    segments = []

    for result in response.results:
        segment_words = []
        for word_info in result.alternatives[0].words:
            segment_words.append(
                WordInfo(
                    word=word_info.word,
                    start_time=word_info.start_time.seconds
                    + word_info.start_time.nanos * 1e-9,
                    end_time=word_info.end_time.seconds
                    + word_info.end_time.nanos * 1e-9,
                    speaker_tag=getattr(word_info, "speaker_tag", None),
                )
            )
        segments.append(
            SegmentInfo(
                transcript=result.alternatives[0].transcript,
                words=segment_words,
                speaker_tag=getattr(
                    result, "speaker_tag", None
                ),  # This might be at result level for diarization
            )
        )
        full_transcript += result.alternatives[0].transcript + " "

    return TranscriptionResponse(
        segments=segments, full_transcript=full_transcript.strip()
    )
