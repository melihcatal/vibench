from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TimestampedTranscriptResponse

def get_timestamped_transcript(job_name: str) -> TimestampedTranscriptResponse:
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    
    job = client.get_recognizer_job(name=job_name)
    if job.state != cloud_speech.RecognizerJob.State.SUCCEEDED:
        raise RuntimeError(f"Job {job_name} is not complete.")
    
    segments = []
    for result in job.results:
        for alternative in result.alternatives:
            segments.append({
                "transcript": alternative.transcript,
                "start_time": result.result_end_offset.total_seconds() - len(alternative.words) * 0.1,
                "end_time": result.result_end_offset.total_seconds(),
                "words": [
                    {
                        "word": word.word,
                        "start_time": word.start_offset.total_seconds(),
                        "end_time": word.end_offset.total_seconds(),
                    }
                    for word in alternative.words
                ],
            })
    
    return TimestampedTranscriptResponse(
        job_name=job_name,
        segments=segments,
        model="latest_long"  # Google Cloud-specific model identifier
    )