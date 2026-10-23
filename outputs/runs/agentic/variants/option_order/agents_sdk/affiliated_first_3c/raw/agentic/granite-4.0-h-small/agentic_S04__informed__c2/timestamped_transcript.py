import os
from speech_client import get_client
from speech_models import BatchTranscriptionStatus

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

def timestamped_transcript(job_id: str) -> dict:
    """Retrieve a completed transcription result with word timestamps.
    Returns the JSON payload containing timestamps for each word/segment.
    """
    client = get_client()
    # Wait until completed (simple poll loop)
    while True:
        status = client.Transcript.get_status(job_id)
        if status == BatchTranscriptionStatus.COMPLETED:
            return client.Transcript.get_result(job_id)
        elif status == BatchTranscriptionStatus.FAILED:
            raise RuntimeError('Transcription job failed')
        time.sleep(5)

if __name__ == "__main__":
    import sys, time
    if len(sys.argv) != 2:
        print('Usage: python timestamped_transcript.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    result = timestamped_transcript(job_id)
    print(result)
