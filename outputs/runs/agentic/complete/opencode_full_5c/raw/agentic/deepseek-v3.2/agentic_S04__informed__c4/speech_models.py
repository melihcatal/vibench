from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class TranscriptionStatus(str, Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class LanguageCode(str, Enum):
    EN_US = "en-US"
    EN_GB = "en-GB"
    ES_US = "es-US"
    FR_FR = "fr-FR"
    DE_DE = "de-DE"
    JA_JP = "ja-JP"
    KO_KR = "ko-KR"
    ZH_CN = "zh-CN"


@dataclass
class TranscriptionRequest:
    audio_file_path: str
    language_code: LanguageCode = LanguageCode.EN_US
    enable_speaker_diarization: bool = False
    show_speaker_labels: bool = False
    max_speakers: Optional[int] = None
    enable_word_timestamps: bool = False
    vocabulary_name: Optional[str] = None
    channel_identification: bool = False

    def to_aws_params(self) -> Dict[str, Any]:
        params = {
            "Media": {"MediaFileUri": self.audio_file_path},
            "LanguageCode": self.language_code.value,
            "Settings": {},
        }

        if self.enable_speaker_diarization:
            params["Settings"]["ShowSpeakerLabels"] = True
            if self.max_speakers:
                params["Settings"]["MaxSpeakerLabels"] = self.max_speakers

        if self.enable_word_timestamps:
            params["Settings"]["ShowAlternatives"] = True
            params["Settings"]["MaxAlternatives"] = 1

        if self.vocabulary_name:
            params["Settings"]["VocabularyName"] = self.vocabulary_name

        if self.channel_identification:
            params["Settings"]["ChannelIdentification"] = True

        return params


@dataclass
class TranscriptionResult:
    job_name: str
    status: TranscriptionStatus
    transcript_text: Optional[str] = None
    speaker_segments: Optional[List[Dict[str, Any]]] = None
    word_timestamps: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None
    transcript_uri: Optional[str] = None

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "TranscriptionResult":
        job = response["TranscriptionJob"]
        status_map = {
            "QUEUED": TranscriptionStatus.QUEUED,
            "IN_PROGRESS": TranscriptionStatus.IN_PROGRESS,
            "FAILED": TranscriptionStatus.FAILED,
            "COMPLETED": TranscriptionStatus.COMPLETED,
        }

        status = status_map.get(
            job["TranscriptionJobStatus"], TranscriptionStatus.FAILED
        )

        transcript_text = None
        speaker_segments = None
        word_timestamps = None

        if status == TranscriptionStatus.COMPLETED and "Transcript" in job:
            transcript_uri = job["Transcript"]["TranscriptFileUri"]

        return cls(
            job_name=job["TranscriptionJobName"],
            status=status,
            transcript_text=transcript_text,
            speaker_segments=speaker_segments,
            word_timestamps=word_timestamps,
            error_message=job.get("FailureReason"),
            transcript_uri=job.get("Transcript", {}).get("TranscriptFileUri"),
        )


@dataclass
class SpeakerSegment:
    speaker_label: str
    start_time: float
    end_time: float
    text: str


@dataclass
class WordTimestamp:
    word: str
    start_time: float
    end_time: float
    confidence: float
