from speech_client import get_speech_client
from speech_models import DiarizationRequest

def get_diarized_transcript(job_id: str) -> dict:
    """
    Requests speaker diarization for a completed AssemblyAI transcription job.
    Returns a dictionary with speaker-labeled segments.
    """
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    
    if transcript.status != "completed":
        raise ValueError(f"Transcription job not completed. Current status: {transcript.status}")
    
    request = DiarizationRequest(transcript_id=job_id)
    response = client.transcripts.diarization(request.to_dict())
    
    return {
        "id": transcript.id,
        "segments": [
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end
            }
            for utterance in response.utterances
        ]
    }