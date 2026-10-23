import os
import requests
from typing import Dict, Any, Optional

from speech_models import (
    TranscriptionRequest,
    TranscriptionResponse,
    DiarizedTranscriptionResponse,
    TimestampedTranscriptionResponse,
)


class SpeechClient:
    def __init__(self):
        self.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
        self.headers = {
            "authorization": self.api_key,
            "content-type": "application/json",
        }
        self.base_url = "https://api.assemblyai.com/v2"

    def submit_transcription(
        self, audio_url: str, speaker_labels: bool = False, timestamps: bool = False
    ) -> TranscriptionResponse:
        payload: Dict[str, Any] = {"audio_url": audio_url}
        if speaker_labels:
            payload["speaker_labels"] = True
        if timestamps:
            payload["word_details"] = True

        response = requests.post(
            f"{self.base_url}/transcript", json=payload, headers=self.headers
        )
        response.raise_for_status()
        data = response.json()
        return TranscriptionResponse(**data)

    def poll_transcription(self, job_id: str) -> TranscriptionResponse:
        response = requests.get(
            f"{self.base_url}/transcript/{job_id}", headers=self.headers
        )
        response.raise_for_status()
        data = response.json()

        if data.get("speaker_labels"):
            return DiarizedTranscriptionResponse(**data)
        if data.get("word_details"):
            return TimestampedTranscriptionResponse(**data)

        return TranscriptionResponse(**data)

    def get_diarized_transcript(
        self, job_id: str
    ) -> Optional[DiarizedTranscriptionResponse]:
        transcript = self.poll_transcription(job_id)
        if (
            isinstance(transcript, DiarizedTranscriptionResponse)
            and transcript.status == "completed"
        ):
            return transcript
        return None

    def get_timestamped_transcript(
        self, job_id: str
    ) -> Optional[TimestampedTranscriptionResponse]:
        transcript = self.poll_transcription(job_id)
        if (
            isinstance(transcript, TimestampedTranscriptionResponse)
            and transcript.status == "completed"
        ):
            return transcript
        return None
