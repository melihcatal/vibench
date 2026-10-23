import json
from speech_client import BatchSTTClient


def get_timestamped_transcript(job_id):
    """Retrieve a transcription result with start/end timestamps per word/segment.

    Args:
        job_id (str): Job ID from a completed transcription job.

    Returns:
        list: List of segments, each containing timestamps and text.
    """
    client = BatchSTTClient()
    response = client.get_job_result(job_id, include_timestamps=True)
    return response.get("segments", [])


# Example (uncomment to test)
# if __name__ == "__main__":
#     job = submit_transcription("sample.wav")  # from submit_transcription.py
#     segments = get_timestamped_transcript(job["job_id"])
#     print(json.dumps(segments, indent=2))
