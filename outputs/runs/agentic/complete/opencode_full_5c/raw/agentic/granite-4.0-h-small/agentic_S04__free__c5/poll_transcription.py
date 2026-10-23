import os
import time
import requests

# provider: Google Cloud Speech-to-Text
API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
BASE_URL = "https://speech.googleapis.com/v1/operations/"


def poll_transcription(job_id, interval=10):
    """
    Poll the transcription job until it completes.
    Returns the transcription result as a dict.
    """
    url = f"{BASE_URL}{job_id}"
    while True:
        response = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        job = response.json()
        if job["done"]:
            if "error" in job:
                raise RuntimeError(f"Transcription failed: {job['error']}")
            result = job["response"]["textAnnotation"]["text"]
            return result
        else:
            print(f"Job {job_id} not complete, waiting {interval}s...")
            time.sleep(interval)
