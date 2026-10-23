from speech_models import TranscriptionResponse, TimestampedTranscript
from poll_transcription import poll_transcription, get_transcript_content
from typing import Optional

def get_timestamped_transcript(job_id: str) -> Optional[TimestampedTranscript]:
    response = poll_transcription(job_id)

    if response.status == "Succeeded" and response.word_timestamps_url:
        print(f"Fetching word-level timestamps from: {response.word_timestamps_url}")
        word_timestamps = get_transcript_content(response.word_timestamps_url)
        return TimestampedTranscript(words=word_timestamps) # Assuming get_transcript_content returns List[WordTimestamp]
    elif response.status == "Succeeded" and not response.word_timestamps_url:
        print(f"Transcription job {job_id} succeeded, but no word timestamps URL was found.")
        return None
    else:
        print(f"Transcription job {job_id} did not succeed or is still in progress. Current status: {response.status}")
        return None
