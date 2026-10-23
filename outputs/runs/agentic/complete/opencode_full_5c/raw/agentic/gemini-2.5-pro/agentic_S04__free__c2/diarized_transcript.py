import os
from speech_client import AssemblyAIClient
from speech_models import TranscriptionResponse


def request_diarized_transcript(audio_url: str) -> str:
    """
    Submits a transcription job with speaker diarization enabled.
    """
    client = AssemblyAIClient()
    options = {
        "speaker_labels": True,
    }
    response = client.submit_transcription(audio_url, options)
    return response.get("id")


if __name__ == "__main__":
    audio_file_url = os.environ.get("EXAMPLE_AUDIO_URL_DIARIZATION")
    if audio_file_url:
        job_id = request_diarized_transcript(audio_file_url)
        print(f"Diarization job submitted with ID: {job_id}")
    else:
        print("Please set the EXAMPLE_AUDIO_URL_DIARIZATION environment variable.")
