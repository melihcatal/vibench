from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import timedelta


@dataclass
class TranscriptionRequest:
    """Local request model for transcription."""

    audio_file_path: str
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    model: str = "default"
    sample_rate_hertz: int = 16000
    encoding: str = "LINEAR16"

    def to_google_config(self):
        """Convert to Google Cloud Speech RecognitionConfig."""
        from google.cloud.speech_v1 import RecognitionConfig

        encoding_map = {
            "LINEAR16": RecognitionConfig.AudioEncoding.LINEAR16,
            "FLAC": RecognitionConfig.AudioEncoding.FLAC,
            "MULAW": RecognitionConfig.AudioEncoding.MULAW,
            "AMR": RecognitionConfig.AudioEncoding.AMR,
            "AMR_WB": RecognitionConfig.AudioEncoding.AMR_WB,
            "OGG_OPUS": RecognitionConfig.AudioEncoding.OGG_OPUS,
            "SPEEX_WITH_HEADER_BYTE": RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE,
        }

        return RecognitionConfig(
            encoding=encoding_map.get(
                self.encoding, RecognitionConfig.AudioEncoding.LINEAR16
            ),
            sample_rate_hertz=self.sample_rate_hertz,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            enable_word_time_offsets=self.enable_word_time_offsets,
            model=self.model,
        )


@dataclass
class TranscriptionResult:
    """Local response model for transcription results."""

    transcript: str
    confidence: float
    language_code: str
    word_timestamps: List[Dict[str, Any]]
    segments: List[Dict[str, Any]]

    @classmethod
    def from_google_response(cls, response, language_code="en-US"):
        """Create from Google Cloud Speech response."""
        transcript_parts = []
        word_timestamps = []
        segments = []

        for result in response.results:
            alternative = result.alternatives[0]
            transcript_parts.append(alternative.transcript)

            segment_words = []
            for word in alternative.words:
                word_data = {
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds(),
                }
                word_timestamps.append(word_data)
                segment_words.append(word_data)

            segment_start = segment_words[0]["start_time"] if segment_words else 0
            segment_end = segment_words[-1]["end_time"] if segment_words else 0

            segments.append(
                {
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence,
                    "start_time": segment_start,
                    "end_time": segment_end,
                    "words": segment_words,
                }
            )

        full_transcript = " ".join(transcript_parts)
        avg_confidence = (
            sum(seg["confidence"] for seg in segments) / len(segments)
            if segments
            else 0
        )

        return cls(
            transcript=full_transcript,
            confidence=avg_confidence,
            language_code=language_code,
            word_timestamps=word_timestamps,
            segments=segments,
        )


@dataclass
class DiarizationConfig:
    """Configuration for speaker diarization."""

    enable_speaker_diarization: bool = True
    min_speaker_count: int = 2
    max_speaker_count: int = 5

    def to_google_config(self):
        """Convert to Google Cloud SpeakerDiarizationConfig."""
        from google.cloud.speech_v1 import SpeakerDiarizationConfig

        return SpeakerDiarizationConfig(
            enable_speaker_diarization=self.enable_speaker_diarization,
            min_speaker_count=self.min_speaker_count,
            max_speaker_count=self.max_speaker_count,
        )
