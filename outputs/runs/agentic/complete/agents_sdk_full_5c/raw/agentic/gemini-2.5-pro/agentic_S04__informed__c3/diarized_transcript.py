from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult, DiarizedUtterance
import assemblyai

def get_diarized_transcript(audio_url: str) -> TranscriptionResult:
    """
    Submits a job with speaker diarization and returns the utterances.
    This function waits for the transcription to complete.
    """
    client = get_assemblyai_client()
    transcriber = client.transcriber
    
    config = assemblyai.TranscriptionConfig(speaker_labels=True)
    
    transcript = transcriber.transcribe(audio_url, config)

    if transcript.status == assemblyai.TranscriptStatus.COMPLETED and transcript.utterances:
        utterances = [
            DiarizedUtterance(
                speaker=str(utt.speaker),
                text=utt.text,
                start=utt.start,
                end=utt.end
            ) for utt in transcript.utterances
        ]
        return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            utterances=utterances
        )
    else:
         return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            text=transcript.error or "Could not retrieve diarized transcript."
        )
