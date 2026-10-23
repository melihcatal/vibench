import os
from speech_client import AssemblyAIClient


def request_timestamped_transcript(audio_url: str) -> str:
    """
    Submits a transcription job and requests word-level timestamps.
    """
    client = AssemblyAIClient()
    options = {
        "word_timestamps": True,
    }
    response = client.submit_transcription(audio_url, options)
    return response.get("id")


if __name__ == "__main__":
    audio_file_url = os.environ.get("EXAMPLE_AUDIO_URL")
    if audio_file_url:
        job_id = request_timestamped_transcript(audio_file_url)
        print(f"Timestamped transcription job submitted with ID: {job_id}")
    else:
        print("Please set the EXAMPLE_AUDIO_URL environment variable.")
