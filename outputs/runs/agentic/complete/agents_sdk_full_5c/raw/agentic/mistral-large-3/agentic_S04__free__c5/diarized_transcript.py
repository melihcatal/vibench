from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import DiarizationResponse

def request_diarization(job_name: str) -> DiarizationResponse:
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    
    job = client.get_recognizer_job(name=job_name)
    if job.state != cloud_speech.RecognizerJob.State.SUCCEEDED:
        raise RuntimeError(f"Job {job_name} is not complete.")
    
    diarization_results = []
    for result in job.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                diarization_results.append({
                    "speaker_tag": word_info.speaker_label,
                    "word": word_info.word,
                    "start_time": word_info.start_offset.total_seconds(),
                    "end_time": word_info.end_offset.total_seconds(),
                })
    
    return DiarizationResponse(
        job_name=job_name,
        diarization=diarization_results,
        model="latest_long"  # Google Cloud-specific model identifier
    )