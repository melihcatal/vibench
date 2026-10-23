import time
import requests
from speech_client import get_batch_client
from speech_models import BatchTranscriptionStatus

# Configurable environment variables for Azure Cognitive Services Speech Service
# Required: AZURE_SPEECH_BATCH_KEY, AZURE_SPEECH_BATCH_REGION

def poll_transcription(job_id, poll_interval=10):
    """Polls the batch transcription job status until completion.

    Args:
        job_id (str): The job identifier returned from submit_transcription.
        poll_interval (int): Seconds to wait between status checks.

    Returns:
        dict: Parsed transcription result payload.
    """
    client = get_batch_client()
    endpoint = client.endpoint
    url = f"{endpoint}/speech/v1.0/transcriptions/{job_id}"
    headers = {
        "Ocp-Apim-Subscription-Key": client.sub_key,
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            if status == "Succeeded":
                return data
            elif status == "Failed":
                raise RuntimeError(f"Transcription job failed: {data.get('error')}")
        elif response.status_code == 202:
            # Still processing
            pass
        else:
            response.raise_for_status()
        time.sleep(poll_interval)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python poll_transcription.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    result = poll_transcription(job_id)
    print("Transcription succeeded:", result)
