import os
import json
from speech_client import BatchSTTClient


def poll_transcription(job_id, timeout=60):
    """Poll a submitted transcription job until completion.

    Args:
        job_id (str): The job ID returned from submission.
        timeout (int): Maximum seconds to wait.

    Returns:
        dict: JSON response containing the transcription result.
    """
    client = BatchSTTClient()
    # Simple polling loop (real impl should handle rate limits)
    while timeout > 0:
        resp = client.get_job_status(job_id)
        if resp.get("status") == "completed":
            return resp
        timeout -= 1
        time.sleep(1)
    raise TimeoutError("Polling timed out for job {}")


# Example (uncomment to test)
# if __name__ == "__main__":
#     job = submit_transcription("sample.wav")  # Assume submit_transcription defined elsewhere
#     result = poll_transcription(job["job_id"])
#     print(json.dumps(result, indent=2))
