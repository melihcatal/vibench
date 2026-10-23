import time
from speech_client import SpeechClient
from speech_models import TranscriptionPollResponse
from assemblyai.types import TranscriptStatus


def poll_transcription(transcript_id: str) -> TranscriptionPollResponse:
    speech_client = SpeechClient()
    # AssemblyAI's get method retrieves the status and result
    transcript = speech_client.client.transcripts.get(transcript_id)

    if transcript.status == TranscriptStatus.completed:
        return TranscriptionPollResponse(
            status=transcript.status.value, text=transcript.text
        )
    else:
        return TranscriptionPollResponse(status=transcript.status.value)
