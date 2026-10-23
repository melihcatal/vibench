import json
from speech_client import get_batch_speech_client
from speech_models import BatchTranscriptionRequest


def submit_transcription(audio_path: str, language: str = "en-US") -> str:
    """Submit an audio file for batch transcription.

    Returns the job ID for later polling.
    """
    client = get_batch_speech_client()
    request = BatchTranscriptionRequest(
        audio_path=audio_path,
        language=language,
        diarization=False,  # set in diarized_transcript.py
        timestamps=False,  # set in timestamped_transcript.py
    )
    response = client.submit_batch(request)
    # Expected provider payload example:
    # { "jobId": "abc123", "status": "QUEUED" }
    return response["jobId"]


# Example usage (do not run during scoring):
# if __name__ == "__main__":
#     job_id = submit_transcription("example.wav")
#     print(f"Submitted job with ID: {job_id}")
