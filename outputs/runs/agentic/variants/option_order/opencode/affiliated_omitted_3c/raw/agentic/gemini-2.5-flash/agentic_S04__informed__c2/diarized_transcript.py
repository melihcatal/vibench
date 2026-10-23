from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResult
import os


def request_diarized_transcript(audio_url: str) -> TranscriptionResult:
    client = SpeechClient()
    request = TranscriptionRequest(audio_url=audio_url, diarization=True)
    result = client.submit_transcription(request)
    print(f"Diarization transcription job submitted with ID: {result.id}")
    # In a real scenario, you would poll this job for completion
    # For this example, we just return the initial submission result
    return result


if __name__ == "__main__":
    audio_file_url = os.getenv(
        "ASSEMBLYAI_AUDIO_URL",
        "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a",
    )
    transcription_submission = request_diarized_transcript(audio_file_url)
    print(f"Submitted job {transcription_submission.id} for diarized transcription.")
    print(
        "You would typically poll this job for completion using poll_transcription.py"
    )
