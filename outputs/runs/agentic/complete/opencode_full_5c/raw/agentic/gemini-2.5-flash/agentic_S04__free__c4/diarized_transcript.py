from google.cloud import speech
from speech_client import get_speech_client, get_gcs_uri
from speech_models import TranscriptionRequest, TranscriptionResult


def request_diarized_transcript(audio_uri: str, language_code: str = "en-US") -> str:
    """
    Submits a transcription job with speaker diarization enabled.
    Returns the operation name.
    """
    client = get_speech_client()
    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Example, adapt to actual audio encoding
        sample_rate_hertz=16000,  # Example, adapt to actual sample rate
        language_code=language_code,
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=6,
        model="latest_long",  # Using a specific model for batch transcription
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(
        f"Diarized transcription job submitted. Operation name: {operation.operation.name}"
    )
    return operation.operation.name


if __name__ == "__main__":
    # Example usage (replace with actual GCS URI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    request_uri = get_gcs_uri("your-gcs-bucket-name", "your-meeting-audio.wav")
    operation_name = request_diarized_transcript(request_uri, "en-US")
    # To get the result, you would poll this operation_name using poll_transcription.py
    # For example:
    # from poll_transcription import poll_transcription_job
    # result = poll_transcription_job(operation_name)
    # print("Diarized Transcript:", result.diarized_segments)
