from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str
    job_name: Optional[str] = None
    speaker_diarization_enabled: bool = False
    word_timestamps_enabled: bool = False

@dataclass
class TranscriptionWord:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None

@dataclass
class TranscriptionSegment:
    id: int
    start_time: float
    end_time: float
    text: str
    words: List[TranscriptionWord] = field(default_factory=list)
    speaker_tag: Optional[int] = None

@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript: str
    segments: List[TranscriptionSegment] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


class TranscriptionNormalizer:
    @staticmethod
    def normalize_aws_transcribe_result(aws_result: Dict[str, Any]) -> TranscriptionResult:
        # This is a simplified normalization. A real implementation would parse the full JSON.
        job_name = aws_result.get("TranscriptionJobName", "")
        job_status = aws_result.get("TranscriptionJobStatus", "")
        transcript_uri = aws_result.get("Transcript", {}).get("TranscriptFileUri", "")

        # In a real scenario, fetch and parse the content from transcript_uri
        # For this example, we'll return placeholder values.
        normalized_transcript = "Normalized transcript from AWS."
        segments = []

        return TranscriptionResult(
            job_id=job_name,
            status=job_status,
            transcript=normalized_transcript,
            segments=segments,
            raw_response=aws_result
        )

    @staticmethod
    def normalize_gcp_speech_result(gcp_response: Any) -> TranscriptionResult:
        # gcp_response is google.cloud.speech_v1p1beta1.types.LongRunningRecognizeResponse
        full_transcript = "".join([result.alternatives[0].transcript for result in gcp_response.results])
        segments = []
        # More sophisticated parsing would be needed for word-level details, diarization etc.

        return TranscriptionResult(
            job_id="gcp_job", # GCP does not have a single job_id like AWS Transcribe for long-running ops
            status="COMPLETED", # Assuming the operation is completed when this is called
            transcript=full_transcript,
            segments=segments,
            raw_response=gcp_response # Store raw response for debugging/completeness
        )

    @staticmethod
    def normalize_azure_speech_result(azure_result: Dict[str, Any]) -> TranscriptionResult:
        # This is a simplified normalization. Azure batch transcription results are complex JSONs.
        normalized_transcript = azure_result.get("text", "")
        return TranscriptionResult(
            job_id="azure_job", # Azure provides a GUID for batch jobs
            status="COMPLETED", # Assuming the operation is completed
            transcript=normalized_transcript,
            segments=[],
            raw_response=azure_result
        )
