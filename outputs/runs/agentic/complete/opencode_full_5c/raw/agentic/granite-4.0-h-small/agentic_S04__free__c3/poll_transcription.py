# poll_transcription.py

from speech_client import get_speech_client
import time, json


def poll_transcription(job_id, timeout=300):
    client = get_speech_client()
    interval = 5
    for _ in range(timeout // interval):
        result = client.get_transcription_job_status(job_id)
        if result["status"] == "COMPLETED":
            return result["transcript_url"]
        elif result["status"] == "FAILED":
            raise RuntimeError("Transcription job failed")
        time.sleep(interval)
    raise TimeoutError("Transcription job timed out")


if __name__ == "__main__":
    import sys, json

    job_id = sys.argv[1]
    url = poll_transcription(job_id)
    print(json.dumps({"transcript_url": url}))
