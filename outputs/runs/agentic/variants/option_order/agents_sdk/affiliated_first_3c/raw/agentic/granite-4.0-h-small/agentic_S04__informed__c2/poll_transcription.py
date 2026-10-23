import time
import os
from speech_client import get_client
from speech_models import BatchTranscriptionStatus

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')


def poll_transcription(job_id: str, timeout: int = 120, interval: int = 5) -> dict:
    """Poll the AssemblyAI transcription job until it completes.
    Returns the final transcript JSON when available.
    Raises TimeoutError if the job does not finish within `timeout` seconds.
    """
    client = get_client()
    end_time = time.time() + timeout
    while time.time() < end_time:
        status = client.Transcript.get_status(job_id)
        if status == BatchTranscriptionStatus.COMPLETED:
            return client.Transcript.get_result(job_id)
        elif status == BatchTranscriptionStatus.FAILED:
            raise RuntimeError('Transcription job failed')
        time.sleep(interval)
    raise TimeoutError('Transcription job timed out')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python poll_transcription.py <job_id> [timeout_seconds]')
        sys.exit(1)
    job_id = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    result = poll_transcription(job_id, timeout=timeout)
    print(result)
