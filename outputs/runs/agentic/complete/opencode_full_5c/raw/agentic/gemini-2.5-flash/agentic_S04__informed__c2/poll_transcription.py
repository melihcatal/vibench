import assemblyai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResponse
import time


def poll_transcription(transcript_id: str) -> TranscriptionResponse:
    client = get_assemblyai_client()
    while True:
        transcript = client.transcripts.get(transcript_id)
        if transcript.status == assemblyai.TranscriptStatus.completed:
            return TranscriptionResponse(
                id=transcript.id,
                status=transcript.status,
                text=transcript.text,
                words=transcript.words,
                utterances=transcript.utterances if transcript.utterances else [],
            )
        elif transcript.status == assemblyai.TranscriptStatus.failed:
            raise Exception(f"Transcription failed: {transcript.error}")
        time.sleep(5)
