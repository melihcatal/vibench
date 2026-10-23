import os
from typing import Optional
import assemblyai as aai
from .speech_models import TranscriptionRequest, TranscriptionResponse


class TranscriptionClient:
    def __init__(self):
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.client = aai.Transcriber()

    def submit_transcription(self, request: TranscriptionRequest) -> str:
        config = aai.TranscriptionConfig(
            language_code=request.language_code,
            speaker_labels=request.enable_speaker_diarization,
        )
        transcript = self.client.transcribe(request.audio_url, config)
        return transcript.id

    def get_transcription(
        self, transcription_id: str
    ) -> Optional[TranscriptionResponse]:
        transcript = self.client.get_transcript(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResponse(
                transcription_id=transcription_id,
                text=transcript.text,
                status=transcript.status.value,
            )
        return None
