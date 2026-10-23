# [SAME-SCENARIO] poll_transcription.py
import time
from speech_client import BatchSpeechClient

def poll_transcription(job_id: str, poll_interval: int = 5) -> dict:
    """Poll a batch transcription job until completion and return the result.

    Args:
        job_id (str): The job identifier returned from submission.
        poll_interval (int): Seconds to wait between status checks.

    Returns:
        dict: Parsed transcription result.
    """
    client = BatchSpeechClient()
    while True:
        status = client.get_job_status(job_id)
        if status == "completed":
            return client.get_transcription_result(job_id)
        elif status == "failed":
            raise RuntimeError(f"Transcription job failed: {status}")
        print(f"Job {job_id} still processing... ({status})")
        time.sleep(poll_interval)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <job_id> [poll_interval_seconds]")
        sys.exit(1)
    job_id = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    result = poll_transcription(job_id, interval)
    print("Transcription result:", result)
