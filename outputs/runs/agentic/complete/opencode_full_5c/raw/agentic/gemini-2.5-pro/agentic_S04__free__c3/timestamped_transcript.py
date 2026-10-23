import os
from speech_client import get_assemblyai_client
from speech_models import TimestampedTranscriptRequest, TimestampedTranscriptResponse


def get_timestamped_transcript(job_id: str) -> TimestampedTranscriptResponse:
    """
    Retrieves the timestamped transcript from a completed AssemblyAI job.
    """
    client = get_assemblyai_client()
    response_data = client.get_transcription(job_id)
    if response_data.get("status") != "completed":
        # In a real app, you would poll until completed
        raise ValueError(
            f"Job {job_id} is not completed. Current status: {response_data.get('status')}"
        )
    return TimestampedTranscriptResponse(**response_data)


if __name__ == "__main__":
    # This is an example, replace with a real COMPLETED transcription ID
    test_completed_job_id = "your_completed_transcription_id_here"
    if "ASSEMBLYAI_API_KEY" not in os.environ:
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    elif test_completed_job_id == "your_completed_transcription_id_here":
        print("Please replace with a real completed job ID.")
    else:
        timestamped_response = get_timestamped_transcript(test_completed_job_id)
        for word in timestamped_response.words:
            print(f"'{word.text}' from {word.start}ms to {word.end}ms")
