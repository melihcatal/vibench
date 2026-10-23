import time
from speech_client import AssemblyAIClient
from speech_models import TranscriptionResponse


def poll_for_transcript(job_id: str) -> TranscriptionResponse:
    """
    Polls an AssemblyAI transcription job until it is completed.

    Args:
        job_id: The ID of the transcription job to poll.

    Returns:
        The completed transcription response object.
    """
    client = AssemblyAIClient()
    while True:
        response = client.get_transcription(job_id)
        if response.status == "completed":
            print("Transcription completed.")
            return response
        elif response.status == "error":
            print(f"Transcription failed: {response.error}")
            raise Exception(f"Transcription failed: {response.error}")
        else:
            print(f"Job status: {response.status}. Polling again in 5 seconds...")
            time.sleep(5)


# Example usage:
# if __name__ == '__main__':
#     # Replace with a real job ID from submit_transcription.py
#     TEST_JOB_ID = "your_job_id_here"
#     try:
#         transcript = poll_for_transcript(TEST_JOB_ID)
#         if transcript.text:
#             print("\nTranscript:")
#             print(transcript.text)
#     except Exception as e:
#         print(e)
