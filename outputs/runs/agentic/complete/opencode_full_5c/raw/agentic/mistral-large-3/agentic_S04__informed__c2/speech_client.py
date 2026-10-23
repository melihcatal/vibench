import os
from typing import Optional, Dict, Any
import assemblyai as aai
from .speech_models import TranscriptionRequest, TranscriptionResponse


class AssemblyAISpeechClient:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
        aai.settings.api_key = self.api_key

    def submit_transcription(self, request: TranscriptionRequest) -> str:
        config = aai.TranscriptionConfig(
            speaker_labels=request.speaker_labels,
            word_timestamps=request.word_timestamps,
        )
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(request.audio_url)
        return transcript.id

    def poll_transcription(self, transcription_id: str) -> TranscriptionResponse:
        transcript = aai.Transcript.get_by_id(transcription_id)
        if transcript.status == aai.TranscriptStatus.error:
            raise ValueError(f"Transcription failed: {transcript.error}")
        return TranscriptionResponse(
            transcription_id=transcript.id,
            status=transcript.status.value,
            text=transcript.text,
            words=transcript.words,
            utterances=transcript.utterances,
        )

    def get_diarized_transcript(self, transcription_id: str) -> Dict[str, Any]:
        transcript = aai.Transcript.get_by_id(transcription_id)
        if not transcript.utterances:
            raise ValueError("No speaker diarization data available")
        return {
            "transcription_id": transcript.id,
            "utterances": [
                {
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                }
                for utterance in transcript.utterances
            ],
        }

    def get_timestamped_transcript(self, transcription_id: str) -> Dict[str, Any]:
        transcript = aai.Transcript.get_by_id(transcription_id)
        if not transcript.words:
            raise ValueError("No word timestamps available")
        return {
            "transcription_id": transcript.id,
            "words": [
                {"text": word.text, "start": word.start, "end": word.end}
                for word in transcript.words
            ],
        }
