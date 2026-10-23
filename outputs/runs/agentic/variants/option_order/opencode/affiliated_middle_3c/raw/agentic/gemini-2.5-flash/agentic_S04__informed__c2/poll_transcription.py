from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult


def poll_transcription_result(job_id: str):
    client = get_assemblyai_client()
    transcript = client.get_transcript(job_id)
    return TranscriptionResult(
        id=transcript.id,
        status=transcript.status,
        text=transcript.text,
        words=transcript.words,
        segments=transcript.segments,
        utterances=transcript.utterances,
    )
