from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai as aai


def get_diarized_transcript(job_id: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    transcript = client.transcriber.get_transcript_by_id(job_id)
    if transcript.speaker_labels:
        return TranscriptionResult(
            id=transcript.id,
            status=transcript.status.value,
            text=transcript.text,
            utterances=[
                {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
                for u in transcript.utterances
            ]
            if transcript.utterances
            else None,
        )
    else:
        # If diarization was not requested or is not available, return a non-diarized transcript
        return TranscriptionResult(
            id=transcript.id, status=transcript.status.value, text=transcript.text
        )
