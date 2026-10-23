# [SAME-SCENARIO] poll_transcription.py
import time
import os
from speech_client import BatchSpeechClient

# Provider used: Azure Cognitive Services Speech-to-Text (Batch API)
client = BatchSpeechClient(
    os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
)


def poll_transcription(job_id: str, interval: int = 15):
    """Periodically poll a batch transcription job until completion.

    Args:
        job_id: Job identifier returned from submit_transcription.
        interval: Seconds to wait between polls.

    Returns:
        dict: Final job status and transcript URL.
    """
    while True:
        status = client.get_transcription_status(job_id)
        if status["state"] == "Succeeded":
            return status
        elif status["state"] == "Failed":
            raise RuntimeError("Transcription job failed")
        time.sleep(interval)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: poll_transcription.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    result = poll_transcription(job_id)
    print(result)
