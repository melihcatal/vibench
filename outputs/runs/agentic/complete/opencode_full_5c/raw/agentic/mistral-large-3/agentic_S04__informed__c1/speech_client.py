import os
from typing import Optional, Dict, Any
import assemblyai as aai
from .speech_models import TranscriptionRequest, TranscriptionResponse


class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
        aai.settings.api_key = self.api_key
        self.client = aai.Transcriber()

    def submit_transcription(self, request: TranscriptionRequest) -> Dict[str, Any]:
        config = aai.TranscriptionConfig(
            speaker_labels=request.speaker_labels,
            word_timestamps=request.word_timestamps,
        )
        transcript = self.client.transcribe(request.audio_url, config)
        return {"id": transcript.id, "status": transcript.status}

    def poll_transcription(
        self, transcription_id: str
    ) -> Optional[TranscriptionResponse]:
        transcript = self.client.get_transcript(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResponse(
                id=transcript.id,
                status=transcript.status.value,
                text=transcript.text,
                words=transcript.words,
                utterances=transcript.utterances,
            )
        return None

    def get_diarized_transcript(
        self, transcription_id: str
    ) -> Optional[TranscriptionResponse]:
        transcript = self.client.get_transcript(transcription_id)
        if (
            transcript.status == aai.TranscriptStatus.completed
            and transcript.utterances
        ):
            return TranscriptionResponse(
                id=transcript.id,
                status=transcript.status.value,
                text=transcript.text,
                words=transcript.words,
                utterances=transcript.utterances,
            )
        return None

    def get_timestamped_transcript(
        self, transcription_id: str
    ) -> Optional[TranscriptionResponse]:
        transcript = self.client.get_transcript(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResponse(
                id=transcript.id,
                status=transcript.status.value,
                text=transcript.text,
                words=transcript.words,
                utterances=transcript.utterances,
            )
        return None
