from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai as aai


def poll_transcription_job(job_id: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    transcript = client.transcriber.get_transcript_by_id(job_id)
    return TranscriptionResult(
        id=transcript.id,
        status=transcript.status.value,
        text=transcript.text,
        words=[
            {"text": w.text, "start": w.start, "end": w.end} for w in transcript.words
        ]
        if transcript.words
        else None,
        utterances=[
            {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
            for u in transcript.utterances
        ]
        if transcript.utterances
        else None,
    )
