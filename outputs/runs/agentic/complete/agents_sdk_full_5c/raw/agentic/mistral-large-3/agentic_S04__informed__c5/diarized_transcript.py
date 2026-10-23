from speech_client import get_speech_client
from speech_models import DiarizationResult

def get_diarized_transcript(job_id: str) -> DiarizationResult:
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.
    Returns a structured diarization result.
    """
    client = get_speech_client()
    
    transcript = client.transcripts.get(job_id)
    
    if transcript.status != "completed":
        raise Exception(f"Transcription job not completed. Current status: {transcript.status}")
    
    if not transcript.utterances:
        raise Exception("No utterances found. Ensure speaker_labels was enabled in the transcription request.")
    
    return DiarizationResult.from_assemblyai_utterances(transcript.utterances)