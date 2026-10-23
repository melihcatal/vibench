import time
import os
from speech_client import SpeechClient

# Provider-specific: Azure Speech Services batch transcription
AZURE_SPEECH_ENDPOINT = os.getenv('AZURE_SPEECH_ENDPOINT')
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')

client = SpeechClient(
    base_url=AZURE_SPEECH_ENDPOINT,
    api_key=AZURE_SPEECH_KEY,
    provider='azure_speech'
)

def poll_transcription(job_id: str, max_attempts: int = 60, interval: int = 5):
    """Poll a batch transcription job until it completes or fails.

    Args:
        job_id (str): The transcription job identifier returned from submit_transcription.
        max_attempts (int): Maximum number of polling attempts.
        interval (int): Seconds to wait between attempts.
    Returns:
        dict: Final job status and transcript URL if successful.
    Raises:
        RuntimeError: If the job fails after max_attempts.
    """
    for attempt in range(1, max_attempts + 1):
        job = client.get(f'/batch/transcriptions/{job_id}')
        status = job.get('status')
        if status == 'Succeeded':
            return job
        if status == 'Failed':
            raise RuntimeError(f'Transcription job {job_id} failed: {job.get("error","Unknown error")}')
        if attempt < max_attempts:
            time.sleep(interval)
    raise RuntimeError(f'Transcription job {job_id} did not complete within {max_attempts} attempts')

if __name__ == '__main__':
    # Example usage
    job_id = 'abc123-0000-1111-2222-xyz'
    result = poll_transcription(job_id)
    print('Job result:', result)
