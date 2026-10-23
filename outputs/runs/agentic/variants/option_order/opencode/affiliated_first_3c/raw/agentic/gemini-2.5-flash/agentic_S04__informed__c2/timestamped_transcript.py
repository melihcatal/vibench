from speech_client import SpeechClient
from speech_models import (
    TranscriptionRequest,
    TranscriptionResponse,
    TranscriptionPollResponse,
)
from assemblyai.types import TranscriptStatus


def request_timestamped_transcript(audio_url: str) -> TranscriptionResponse:
    speech_client = SpeechClient()
    # AssemblyAI's create method with word_timestamps enabled
    transcript = speech_client.client.transcripts.create(
        audio_url=audio_url, word_timestamps=True
    )
    return TranscriptionResponse(id=transcript.id, status=transcript.status.value)


def get_timestamped_transcript(transcript_id: str) -> TranscriptionPollResponse:
    speech_client = SpeechClient()
    transcript = speech_client.client.transcripts.get(transcript_id)

    if transcript.status == TranscriptStatus.completed and transcript.words:
        return TranscriptionPollResponse(
            status=transcript.status.value,
            text=transcript.text,
            words=[w.dict() for w in transcript.words],
        )
    else:
        return TranscriptionPollResponse(status=transcript.status.value)
