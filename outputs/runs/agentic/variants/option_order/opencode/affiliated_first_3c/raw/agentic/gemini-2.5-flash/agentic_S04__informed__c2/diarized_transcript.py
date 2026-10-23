from speech_client import SpeechClient
from speech_models import (
    TranscriptionRequest,
    TranscriptionResponse,
    TranscriptionPollResponse,
)
from assemblyai.types import TranscriptStatus


def request_diarized_transcript(audio_url: str) -> TranscriptionResponse:
    speech_client = SpeechClient()
    # AssemblyAI's create method with speaker_diarization enabled
    transcript = speech_client.client.transcripts.create(
        audio_url=audio_url, speaker_diarization=True
    )
    return TranscriptionResponse(id=transcript.id, status=transcript.status.value)


def get_diarized_transcript(transcript_id: str) -> TranscriptionPollResponse:
    speech_client = SpeechClient()
    transcript = speech_client.client.transcripts.get(transcript_id)

    if transcript.status == TranscriptStatus.completed and transcript.utterances:
        # Format utterances for diarized output
        diarized_text = "\n".join(
            [f"Speaker {u.speaker}: {u.text}" for u in transcript.utterances]
        )
        return TranscriptionPollResponse(
            status=transcript.status.value,
            text=diarized_text,
            utterances=[u.dict() for u in transcript.utterances],
        )
    else:
        return TranscriptionPollResponse(status=transcript.status.value)
