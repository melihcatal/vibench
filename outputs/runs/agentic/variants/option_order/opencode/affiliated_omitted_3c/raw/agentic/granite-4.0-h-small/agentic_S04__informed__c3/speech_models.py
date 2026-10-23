# Local request/response helpers and normalization helpers for Batch Speech-to-Text
import json
from typing import Any, Dict, List


class TranscribeRequest:
    def __init__(
        self,
        job_name: str,
        audio_uri: str,
        language_code: str = "en-US",
        vocab_name: str = None,
        diarization: Dict = None,
    ):
        self.job_name = job_name
        self.audio_uri = audio_uri
        self.language_code = language_code
        self.vocab_name = vocab_name
        self.diarization = diarization  # e.g. {"MaxSpeakers": 5}

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "TranscriptionJobName": self.job_name,
            "LanguageCode": self.language_code,
            "Media": {"MediaFileUri": self.audio_uri},
            "MediaFormat": "mp3",
        }
        if self.vocab_name:
            payload["VocabularyName"] = self.vocab_name
        if self.diarization:
            payload["DiarizationConfig"] = self.diarization
        return payload


class TranscribeResponse:
    def __init__(self, data: Any):
        self.raw = data
        self.job = data["TranscriptionJob"]
        self.status = self.job["TranscriptionJobStatus"]
        self.transcript_uri = None
        if self.status == "COMPLETED":
            self.transcript_uri = self.job["Transcript"]["TranscriptFileUri"]
        self.failure_reason = self.job.get("FailureReason")

    def is_failed(self) -> bool:
        return self.status == "FAILED"

    def is_completed(self) -> bool:
        return self.status == "COMPLETED"

    def get_transcript(self) -> str:
        if self.transcript_uri:
            # simple fetch for demo; replace with S3 download logic
            return self.fetch_s3_uri(self.transcript_uri)
        return None

    def fetch_s3_uri(self, uri: str) -> str:
        import boto3, botocore

        s3 = boto3.client("s3")
        try:
            obj = s3.get_object(
                Bucket=uri.split("/")[2], Key="/".join(uri.split("/")[3:])
            )
            return obj["Body"].read().decode("utf-8")
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"S3 fetch error: {e}")


class TranscribeTimestampResponse:
    def __init__(self, raw_segments: List):  # raw list from timestamped JSON response
        self.segments = []
        for seg in raw_segments:
            self.segments.append(
                {
                    "text": seg["alternatives"][0]["content"],
                    "start": seg.get("start_time"),
                    "end": seg.get("end_time"),
                }
            )

    def to_json(self) -> str:
        return json.dumps({"segments": self.segments})
