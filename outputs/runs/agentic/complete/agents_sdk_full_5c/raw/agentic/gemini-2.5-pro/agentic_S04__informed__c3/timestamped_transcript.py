from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult, WordTimestamp
import assemblyai

def get_timestamped_transcript(audio_url: str) -> TranscriptionResult:
    """
    Submits a job and returns word-level timestamps.
    This function waits for the transcription to complete.
    """
    client = get_assemblyai_client()
    transcriber = client.transcriber
    
    # word_details=True is the default and not strictly necessary to set
    config = assemblyai.TranscriptionConfig() 

    transcript = transcriber.transcribe(audio_url, config)
    
    if transcript.status == assemblyai.TranscriptStatus.COMPLETED and transcript.words:
        words = [
            WordTimestamp(
                text=word.text,
                start=word.start,
                end=word.end,
                confidence=word.confidence
            ) for word in transcript.words
        ]
        return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            words=words,
            text=transcript.text
        )
    else:
        return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            text=transcript.error or "Could not retrieve timestamped transcript."
        )
