import os
from speech_client import get_assemblyai_client
from speech_models import TranscriptionSubmit, TranscriptionResponse


def submit_transcription_job(audio_url: str) -> TranscriptionResponse:
    """
    Submits a new transcription job to AssemblyAI.
    """
    client = get_assemblyai_client()
    submit_request = TranscriptionSubmit(audio_url=audio_url)
    response_data = client.submit_transcription(submit_request.audio_url)
    return TranscriptionResponse(**response_data)


if __name__ == "__main__":
    # This is an example, replace with a real audio url
    audio_url = "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a"
    if "ASSEMBLYAI_API_KEY" not in os.environ:
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    else:
        transcription_response = submit_transcription_job(audio_url)
        print(f"Transcription submitted with ID: {transcription_response.id}")
