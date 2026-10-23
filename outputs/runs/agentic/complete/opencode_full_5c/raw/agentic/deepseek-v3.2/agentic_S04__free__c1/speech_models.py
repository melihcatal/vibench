from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json


@dataclass
class TranscriptionRequest:
    """Local model for transcription request."""

    audio_file_path: str
    language_code: str = "en-US"
    enable_word_time_offsets: bool = True
    enable_speaker_diarization: bool = False
    min_speaker_count: Optional[int] = None
    max_speaker_count: Optional[int] = None
    model: str = "video"


@dataclass
class WordTimestamp:
    """Local model for word timestamp."""

    word: str
    start_time: float
    end_time: float


@dataclass
class TranscriptionSegment:
    """Local model for transcription segment."""

    transcript: str
    start_time: float
    end_time: float
    words: List[WordTimestamp]
    speaker_tag: Optional[int] = None


@dataclass
class TranscriptionResult:
    """Local model for transcription result."""

    operation_name: str
    segments: List[TranscriptionSegment]
    full_transcript: str
    language_code: str


def normalize_transcription_response(google_response, operation_name, language_code):
    """Normalize Google Cloud Speech-to-Text response to local model."""
    segments = []
    full_transcript_parts = []

    for result in google_response.results:
        alternative = result.alternatives[0]

        segment = TranscriptionSegment(
            transcript=alternative.transcript,
            start_time=alternative.words[0].start_time.total_seconds()
            if alternative.words
            else 0,
            end_time=alternative.words[-1].end_time.total_seconds()
            if alternative.words
            else 0,
            words=[],
        )

        if alternative.words:
            for word_info in alternative.words:
                segment.words.append(
                    WordTimestamp(
                        word=word_info.word,
                        start_time=word_info.start_time.total_seconds(),
                        end_time=word_info.end_time.total_seconds(),
                    )
                )

        segments.append(segment)
        full_transcript_parts.append(alternative.transcript)

    return TranscriptionResult(
        operation_name=operation_name,
        segments=segments,
        full_transcript=" ".join(full_transcript_parts),
        language_code=language_code,
    )


def result_to_json(transcription_result):
    """Convert transcription result to JSON."""
    return json.dumps(
        {
            "operation_name": transcription_result.operation_name,
            "full_transcript": transcription_result.full_transcript,
            "language_code": transcription_result.language_code,
            "segments": [
                {
                    "transcript": segment.transcript,
                    "start_time": segment.start_time,
                    "end_time": segment.end_time,
                    "speaker_tag": segment.speaker_tag,
                    "words": [
                        {
                            "word": word.word,
                            "start_time": word.start_time,
                            "end_time": word.end_time,
                        }
                        for word in segment.words
                    ],
                }
                for segment in transcription_result.segments
            ],
        },
        indent=2,
    )
