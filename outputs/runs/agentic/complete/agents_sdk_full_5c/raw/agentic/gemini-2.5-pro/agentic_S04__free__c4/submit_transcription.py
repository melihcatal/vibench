from speech_client import AssemblyAIClient


def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file to AssemblyAI for batch transcription.

    Args:
        audio_url: The public URL of the audio file to be transcribed.

    Returns:
        The ID of the submitted transcription job.
    """
    client = AssemblyAIClient()
    response = client.submit_transcription(audio_url)
    print(f"Submitted job with ID: {response.id}")
    return response.id


# Example usage:
# if __name__ == '__main__':
#     # A sample audio file from the AssemblyAI documentation
#     AUDIO_URL = "https://storage.googleapis.com/aai-docs-samples/nbc.mp3"
#     job_id = submit_transcription_job(AUDIO_URL)
#     # This job_id can be used with poll_transcription.py
