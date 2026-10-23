from speech_client import get_assemblyai_client
from speech_models import TranscriptionResponse

def poll_transcription(transcript_id: str) -> TranscriptionResponse:
    client = get_assemblyai_client()
    transcript = client.transcripts.get(transcript_id)
    if transcript.status == "completed":
        return TranscriptionResponse(
            transcript_id=transcript.id,
            status=transcript.status,
            text=transcript.text,
            words=transcript.words,
            utterances=transcript.utterances
        )
    elif transcript.status == "failed":
        raise ValueError(f"Transcription failed: {transcript.error}")
    else:
        raise TimeoutError(f"Transcription not ready. Status: {transcript.status}")