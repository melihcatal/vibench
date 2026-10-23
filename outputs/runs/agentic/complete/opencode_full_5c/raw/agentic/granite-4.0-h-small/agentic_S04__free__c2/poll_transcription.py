import time
from speech_client import get_batch_speech_client
from speech_models import TranscriptionJobStatus


def poll_transcription(job_id: str, interval: int = 10) -> dict:
    """Poll a batch transcription job until completion.

    Returns the full result payload.
    """
    client = get_batch_speech_client()
    while True:
        result = client.get_batch_status(job_id)
        status = result.get("status")
        if status == TranscriptionJobStatus.COMPLETED:
            return result
        elif status == TranscriptionJobStatus.FAILED:
            raise RuntimeError(
                f"Batch job failed: {result.get('error', 'unknown error')}"
            )
        print(f"Job {job_id} is {status}. Waiting {interval}s...")
        time.sleep(interval)


# Example usage (not executed during scoring):
# if __name__ == "__main__":
#     result = poll_transcription("abc123")
#     print(result)
