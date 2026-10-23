from typing import Optional, Dict, Any
import os
import time
import assemblyai as aai
from dataclasses import dataclass


@dataclass
class TranscriptionConfig:
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False


@dataclass
class TranscriptionResult:
    id: str
    status: str
    transcript: Optional[str] = None
    words: Optional[list] = None
    utterances: Optional[list] = None
    error: Optional[str] = None


class SpeechClient:
    def __init__(self):
        self.client = aai.Client(api_key=os.getenv("ASSEMBLYAI_API_KEY"))

    def submit_transcription(self, config: TranscriptionConfig) -> TranscriptionResult:
        transcript_params = {
            "audio_url": config.audio_url,
            "speaker_labels": config.speaker_labels,
            "word_timestamps": config.word_timestamps,
        }
        transcript = self.client.transcripts.submit(**transcript_params)
        return TranscriptionResult(id=transcript.id, status="submitted")

    def poll_transcription(self, transcription_id: str) -> TranscriptionResult:
        transcript = self.client.transcripts.get(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return TranscriptionResult(
                id=transcript.id,
                status="completed",
                transcript=transcript.text,
                words=transcript.words,
                utterances=transcript.utterances,
            )
        elif transcript.status == aai.TranscriptStatus.error:
            return TranscriptionResult(
                id=transcript.id,
                status="failed",
                error=transcript.error,
            )
        else:
            return TranscriptionResult(id=transcript.id, status="processing")

    def get_diarized_transcript(self, transcription_id: str) -> Optional[list]:
        transcript = self.client.transcripts.get(transcription_id)
        if (
            transcript.status == aai.TranscriptStatus.completed
            and transcript.utterances
        ):
            return [
                {
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                }
                for utterance in transcript.utterances
            ]
        return None

    def get_timestamped_transcript(self, transcription_id: str) -> Optional[list]:
        transcript = self.client.transcripts.get(transcription_id)
        if transcript.status == aai.TranscriptStatus.completed and transcript.words:
            return [
                {
                    "word": word.text,
                    "start": word.start,
                    "end": word.end,
                }
                for word in transcript.words
            ]
        return None
