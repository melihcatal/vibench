# speech_models.py

from typing import TypedDict, List

TTranscript = TypedDict(
    "TTranscript",
    {
        "job_id": str,
        "status": str,
        "transcript_url": str,
    },
)

TJobStatus = TypedDict(
    "TJobStatus",
    {
        "job_id": str,
        "status": str,
    },
)


class TTimestampedResult(TypedDict):
    segments: List[dict]


# Example request/response models for internal use


class TBatchRequest(TypedDict):
    audio_file: str
    language_code: str
    features: dict
    output_format: str


class TBatchResponse(TypedDict):
    job_id: str


TTranslationRequest = TypedDict(
    "TTranslationRequest", {"text": str, "target_language": str}
)

TTranslationResult = TypedDict("TTranslationResult", {"translated_text": str})
