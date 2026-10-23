import os
import time
import json
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobStatus, PollJobResponse

# ------------------------------------------------------------
# poll_transcription.py
# Poll a submitted batch transcription job and return the result URL
# ------------------------------------------------------------

def poll_transcription(job_id: str, interval: float = 5.0) -> str:
    """Poll the transcription job until it completes.

    Returns the download URL for the JSON transcript when status is 'Succeeded'.
    Raises RuntimeError if the job fails or times out.
    """
    client = BatchSpeechClient()
    start = time.time()
    while True:
        status_resp = client.get_transcription_job(job_id)
        status = status_resp.status  # enum value of TranscriptionJobStatus
        if status == TranscriptionJobStatus.Succeeded:
            return status_resp.results_url
        if status == TranscriptionJobStatus.Failed:
            raise RuntimeError(f"Transcription job {job_id} failed.")
        if time.time() - start > 600:  # 10 minute timeout
            raise TimeoutError("Transcription job timed out.")
        time.sleep(interval)

# Example usage (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Poll a batch transcription job.")
    parser.add_argument("job_id", help="Job ID returned from submit_transcription.")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds.")
    args = parser.parse_args()
    url = poll_transcription(args.job_id, args.interval)
    print(url)
