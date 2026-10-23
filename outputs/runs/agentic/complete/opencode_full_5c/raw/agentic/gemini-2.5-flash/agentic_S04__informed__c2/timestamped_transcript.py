import assemblyai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResponse


def get_timestamped_transcript(transcript_id: str) -> dict:
    client = get_assemblyai_client()
    transcript = client.transcripts.get(transcript_id)
    if transcript.status == assemblyai.TranscriptStatus.completed:
        return {
            "words": [
                {"text": w.text, "start": w.start, "end": w.end}
                for w in transcript.words
            ],
            "utterances": [
                {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
                for u in transcript.utterances
            ]
            if transcript.utterances
            else [],
        }
    elif transcript.status == assemblyai.TranscriptStatus.failed:
        raise Exception(f"Transcription failed: {transcript.error}")
    else:
        raise Exception(f"Transcription status is {transcript.status}, not completed.")
