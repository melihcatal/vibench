from speech_models import TranscriptionResponse, DiarizationResult
from poll_transcription import poll_transcription, get_transcript_content
from typing import Optional

def get_diarized_transcript(job_id: str) -> Optional[DiarizationResult]:
    response = poll_transcription(job_id)
    
    if response.status == "Succeeded" and response.diarization_result_url:
        print(f"Fetching diarized transcript from: {response.diarization_result_url}")
        diarized_segments = get_transcript_content(response.diarization_result_url)
        return DiarizationResult(segments=diarized_segments) # Assuming get_transcript_content returns List[TranscriptSegment]
    elif response.status == "Succeeded" and not response.diarization_result_url:
        print(f"Transcription job {job_id} succeeded, but no diarization result URL was found.")
        return None
    else:
        print(f"Transcription job {job_id} did not succeed or is still in progress. Current status: {response.status}")
        return None
