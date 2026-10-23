import json
from typing import Literal, Optional, Dict, Any, List

from pydantic import BaseModel, Field


class TranscriptionJobPayload(BaseModel):
    language_code: str = Field(..., example="en-US")
    audio_uri: str = Field(..., example="s3://your-bucket/your-audio.flac")
    job_name: Optional[str] = None
    output_bucket_name: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class TranscriptionJobResult(BaseModel):
    job_id: str
    status: str  # e.g., SUBMITTED, IN_PROGRESS, COMPLETED, FAILED
    transcript_uri: Optional[str] = None
    language_code: Optional[str] = None
    creation_time: Optional[str] = None
    completion_time: Optional[str] = None
    failure_reason: Optional[str] = None


class DiarizationRequest(BaseModel):
    job_id: str
    max_speakers: int = 2
    min_speakers: int = 2


class TimestampedTranscriptRequest(BaseModel):
    job_id: str


class TranslateRequest(BaseModel):
    text: str
    source_language_code: str
    target_language_code: str


class ModerateRequest(BaseModel):
    text: str
    language_code: str = "en"


class SummarizeRequest(BaseModel):
    transcript_text: str
    max_tokens: int = 500
    model_id: str = "anthropic.claude-v2"


class EmbedRequest(BaseModel):
    text_segments: List[str]
    model_id: str = "amazon.titan-embed-text-v1"


def parse_transcription_result(transcript_uri: str) -> dict:
    # This is a placeholder. In a real scenario, this would involve
    # fetching the content from the S3 URI and parsing the JSON.
    # For this exercise, we'll return a mock structure.
    return {
        "results": [
            {
                "alternatives": [
                    {
                        "transcript": "This is a sample transcript.",
                        "words": [
                            {"start_time": "0.1", "end_time": "0.5", "word": "This"},
                            {"start_time": "0.5", "end_time": "0.6", "word": "is"},
                            {"start_time": "0.6", "end_time": "0.7", "word": "a"},
                            {"start_time": "0.7", "end_time": "1.2", "word": "sample"},
                            {"start_time": "1.2", "end_time": "1.8", "word": "transcript."},
                        ],
                    }
                ]
            }
        ]
    }
